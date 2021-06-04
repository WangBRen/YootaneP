
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" Back-end to run quantum program on Quantum device of Institute Of Physics(IOP)."""
import math
import random
import json

from projectq.cengines import BasicEngine
from projectq.meta import get_control_count, LogicalQubitIDTag
from projectq.ops import (NOT,
                          Y,
                          Z,
                          T,
                          Tdag,
                          S,
                          Sdag,
                          H,
                          Rx,
                          Ry,
                          Rz,
                          Measure,
                          Allocate,
                          Deallocate,
                          Barrier,
                          FlushGate)

from ._iop_http_client import send, retrieve, send_to_iop


class IOPBackend(BasicEngine):
    """
    The IOP Backend class, which stores the circuit, transforms it to JSON,
    and sends the circuit through the IOP API.
    """
    def __init__(self, use_hardware=False, num_runs=1024, verbose=True,
                 token='', device='IOP_01',
                 num_retries=3000, interval=1,
                 retrieve_execution=None):
        """
        Initialize the Backend object.

        Args:
            use_hardware (bool): If True, the code is run on the IBM quantum
                chip (instead of using the HiQ simulator)
            num_runs (int): Number of runs to collect statistics.
                (default is 1024)
            verbose (bool): If True, statistics are printed, in addition to
                the measurement result being registered (at the end of the
                circuit).
            token (str): IOP quantum experience user password.
            device (str): name of the IBM device to use. IOP_01 By default
            num_retries (int): Number of times to retry to obtain
                results from the IOP API. (default is 3000)
            interval (float, int): Number of seconds between successive
                attempts to obtain results from the IOP API.
                (default is 1)
            retrieve_execution (int): Job ID to retrieve instead of re-
                running the circuit (e.g., if previous run timed out).
        """
        BasicEngine.__init__(self)
        self._reset()
        if use_hardware:
            self.device = device
        else:
            self.device = 'HiQ_simulator'
        self._num_runs = num_runs
        self._verbose = verbose
        self._token=token
        self._num_retries = num_retries
        self._interval = interval
        self._probabilities = dict()
        # self.qasm = ""
        self._json=[]
        self._allocated_qubits = set()
        
        self._map = dict()
        self._circ= {}
        self._Meas=[]
        self._Qbs=[]
        self._layers={}
        self.iopqasm ={}
        self._retrieve_execution = retrieve_execution

    def is_available(self, cmd):
        ## To do: add the all quantum gate which can be implemented
        """
        Return true if the command can be executed.

        The IOP quantum chip can only do U1,U2,U3,barriers, and CX / CNOT.
        Conversion implemented for Rotation gates and H gates.

        Args:
            cmd (Command): Command for which to check availability
        """
        g = cmd.gate
        if g == NOT and get_control_count(cmd) == 1:
            return True
        if get_control_count(cmd) == 0:
            if g == H:
                return True
            if isinstance(g, (Rx, Ry, Rz)):
                return True
        if g in (Measure, Allocate, Deallocate):
            return True
        return False

    def get_qasm(self):
        """ Return the IOPQASM representation of the circuit sent to the backend.
        Should be called AFTER calling the ibm device """
        return self.iopqasm

    def _reset(self):
        """ Reset all temporary variables (after flush gate). """
        self._clear = True
        self._measured_ids = []

    def _store(self, cmd):
        """
        Temporarily store the command cmd.

        Translates the command and stores it in a local variable (self._cmds).

        Args:
            cmd: Command to store
        """
        if self._clear:
            self._probabilities = dict()
            self._clear = False
            self.iopqasm = ""
            self._json=[]
            self._map = dict()
            self._circ = {}
            self._Meas = []
            self._Qbs = []
            self._layers = {}

        gate = cmd.gate
        if gate == Allocate:
            qubit_id = cmd.qubits[0][0].id
            if qubit_id not in self._map:
                self._map[qubit_id] = qubit_id
            self._layers[qubit_id] = 0

        elif gate == Deallocate:
            pass

        elif gate == Measure:
            assert len(cmd.qubits) == 1 and len(cmd.qubits[0]) == 1
            qb_id = cmd.qubits[0][0].id
            self._Meas.append(qb_id)

        elif gate == NOT and get_control_count(cmd) == 1:
            ctrl_pos = cmd.control_qubits[0].id
            qb_pos = cmd.qubits[0][0].id
            depth=max(self._layers[qb_pos],self._layers[ctrl_pos])
            self._layers[qb_pos]=depth+1
            self._layers[ctrl_pos]=depth+1
            if depth==0:
                self._circ[depth + 1]=[['cnot',[ctrl_pos,qb_pos]]]
            else:
                self._circ[depth + 1].append(['cnot',[ctrl_pos,qb_pos]])

        elif isinstance(gate, (Rx, Ry, Rz)):
            assert get_control_count(cmd) == 0
            qb_pos = cmd.qubits[0][0].id
            depth=self._layers[qb_pos]
            self._layers[qb_pos] = depth + 1
            if depth==0:
                self._circ[depth + 1] =[[str(gate),depth+1,gate.angle]]
            else:
                self._circ[depth + 1] .append([str(gate), depth + 1, gate.angle])

        elif gate == H:
            qb_pos = cmd.qubits[0][0].id
            depth = self._layers[qb_pos]
            self._layers[qb_pos] = depth + 1
            if depth == 0:
                self._circ[depth + 1] = [['h', depth + 1, 0]]
            else:
                self._circ[depth + 1].append(['h', depth + 1,0])
        else:
            raise Exception('Command not authorized. You should run the circuit with the appropriate iop setup.')

    def _logical_to_physical(self, qb_id):
        pass
        ## To do: Add the mapper function for IOP device

    def get_probabilities(self, qureg):
        """
        Return the list of basis states with corresponding probabilities.
        If input qureg is a subset of the register used for the experiment,
        then returns the projected probabilities over the other states.

        The measured bits are ordered according to the supplied quantum
        register, i.e., the left-most bit in the state-string corresponds to
        the first qubit in the supplied quantum register.

        Warning:
            Only call this function after the circuit has been executed!

        Args:
            qureg (list<Qubit>): Quantum register determining the order of the
                qubits.

        Returns:
            probability_dict (dict): Dictionary mapping n-bit strings to
                probabilities.

        Raises:
            RuntimeError: If no data is available (i.e., if the circuit has
                not been executed). Or if a qubit was supplied which was not
                present in the circuit (might have gotten optimized away).
        """
        if len(self._probabilities) == 0:
            raise RuntimeError("Please, run the circuit first!")

        probability_dict = dict()
        for state in self._probabilities:
            mapped_state = ['0'] * len(qureg)
            for i in range(len(qureg)):
                mapped_state[i] = state[self._logical_to_physical(qureg[i].id)]
            probability = self._probabilities[state]
            mapped_state = "".join(mapped_state)
            if mapped_state not in probability_dict:
                probability_dict[mapped_state] = probability
            else:
                probability_dict[mapped_state] += probability
        return probability_dict

    def _run(self):
        """
        Run the circuit.

        Send the circuit via IOP API (using JSON written
        circuits) using the provided user data / ask for the user token.
        """
        print(self._circ)
        print(self._Meas)
        print(self._map)
        self.iopqasm['Operators']= self._circ
        self.iopqasm['Measure']= self._Meas
        self.iopqasm['Qubits']= self._map
        self._json.append([self._circ[i] for i in self._circ])
        self._json.append(self._Meas)
        self._json.apped([Q_id for Q_id in self._map])
        max_qubit_id=max([Q_id for Q_id in self._map])

        info = {}
        info['json']=self._json
        info['nq']=max_qubit_id
        info['shots'] = self._num_runs
        info['maxCredits'] = 10
        info['backend'] = {'name': self.device}

        data = info['json']

        print(info)
        try:
            if self._retrieve_execution is None:
                # res = send(info, device=self.device,
                #            token=self._token,
                #            num_retries=self._num_retries,
                #            interval=self._interval,
                #            verbose=self._verbose)
                res = send_to_iop(data)
            else:
                res = retrieve(device=self.device,
                               token=self._token,
                               jobid=self._retrieve_execution,
                               num_retries=self._num_retries,
                               interval=self._interval,
                               verbose=self._verbose)
            counts = res['data']['counts']
            # Determine random outcome
            P = random.random()
            p_sum = 0.
            measured = ""
            length=len(self._measured_ids)
            for state in counts:
                probability = counts[state] * 1. / self._num_runs
                state="{0:b}".format(int(state,0))
                state=state.zfill(max_qubit_id)

                state=state[::-1]
                p_sum += probability
                star = ""
                if p_sum >= P and measured == "":
                    measured = state
                    star = "*"
                self._probabilities[state] = probability
                if self._verbose and probability > 0:
                    print(str(state) + " with p = " + str(probability) +
                          star)
        except TypeError:
            raise Exception("Failed to run the circuit. Aborting.")

    def receive(self, command_list):
        """
        Receives a command list and, for each command, stores it until
        completion.

        Args:
            command_list: List of commands to execute
        """
        for cmd in command_list:
            if not cmd.gate == FlushGate():
                self._store(cmd)
            else:
                self._run()
                self._reset()
