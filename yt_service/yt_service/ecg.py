# Load NeuroKit and other useful packages
import neurokit2 as nk#
import pandas as pd

# Retrieve ECG data from data folder (sampling rate= 1000 Hz)
#ecg_signal = nk.data(dataset="ecg_3000hz")['ECG']
#np.savetxt('ECGdata.csv', ecg_signal, delimiter=",")

def ecg(dataset):
    # dataset = pd.read_csv(r"./data.csv",)#read data 
    #Calculate moving average with 0.75s in both directions, then append do dataset
    print(dataset)
    ecg_signal = nk.ecg_clean(dataset,method='neurokit')
    # Extract R-peaks locations
    print(ecg_signal)
    _, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=500,method="neurokit")
    print(rpeaks)
    # Zooming into the first 5 R-peaks
                    
    # Delineate the ECG signal and visualizing all peaks of ECG complexes

    _, waves_peak = nk.ecg_delineate(ecg_signal, rpeaks, sampling_rate=500, method="peak", show=True, show_type='all')
    print(waves_peak)
    # Delineate the ECG signal
    return waves_peak
