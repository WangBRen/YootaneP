import requests

def trans_op(self):
    #op转义函数，在‘前加两个反斜杠
    #op为operation简写，即每个操作
    if self == 'X':
        return "\\'X\\'"
    if self == 'Z':
        return "\\'Z\\'"
    if self == 'Y':
        return "\\'Y\\'"
    if self == "H":
        return "\\'H\\'"
    if self == 'Rx':
        return "\\'Rx\\'"
    if self == 'Ry':
        return "\\'Ry\\'"
    if self == 'Rz':
        return "\\'Rz\\'"
    if self == 'T':
        return "\\'T\\'"
    if self == 'CNOT':
        return "\\'CNOT\\'"
    if self == 'ISWAP':
        return "\\'ISWAP\\'"

def trans_iop_str(self, nqubits = 3 , layers = 4 ):

##nqubits定义可以操作的量子比特数    
##layers线路层数
    op_list = self["blocks"]
    n=len(op_list)
    last_iop = []
    mea = []
    hiq_list=[[[] for col in range(10)] for row in range(10)]
    for k in range(n-1):
        for i in range(n-1-k):
            if op_list[i]['pos'][0]>op_list[i+1]['pos'][0]:
                op_list[i],op_list[i+1] = op_list[i+1],op_list[i]
    
    r = [0] * nqubits
    l = [0] * layers

    op = [[]]*layers
    

    for i in range(n):
            k = op_list[i]['pos'][0]
            # k为线路深度即操作处在线路第几层
            j = op_list[i]['pos'][1]
            # j为量子比特位
            hiq_list[k][j] = op_list[i]['type']           

            for h in range(nqubits):
                if  j == h:
                    op_or = hiq_list[k][j]
                    #op_or未处理的操作
                    op_add = trans_op(op_or)
                    #op_add加转义符后的操作
                    if op_or == 'Measure':
                        mea.append(j)
                        continue
    #                 op += "\\"
                    op_str = "["
                    op_str += op_add
                    op_str += ","
                    op_str += str(j)
                    op_str += ","
                    if op_list[i]['ctrls'] == []:
                        para = 0
                    else: 
                        para = op_list[i]['ctrls'][0]

                    op_str += str(para)
                    op_str += "]"
                    r[h] += 1
                    #判定用到了哪几个比特位，在这个比特上作用一次就加一
                    if r[h] <= 1:
                        last_iop.append(j) 
                    op_h = op_str
                
            for layer in range(layers):
                op_or = hiq_list[k][j]
                if op_or == 'Measure':
                    l[k] += -1
                if k == layer:
                    l[k] += 1
                    if l[k] <= 1:
                        op[layer] = "["
                        op[layer] += op_str
                    if l[k] >1:
                        op[layer] += ","
                        op[layer] += op_str
                    op_str = ""
                    #刷新op_str


    for layer in range(layers):
        op[layer] += "],"
        if l[layer] <= 0:
            op[layer] = ""

    
    op_last = ""
    for layer in range(layers):
        op_last += op[layer]
        
    op_last += str(mea)
    op_last += ","
    op_last += str(last_iop)

        
            
    return  op_last

def getResult(data):
    print(data)
    body = trans_iop_str(data)
    print(body)
    # return body
    request_body = {
            # 'qtasm': "[[\\'H\\',0,0]],[0],[0]",
            "qtasm": "[['H',0,0]],[['CNOT',[0,1]]],[['CNOT',[1,2]]],[0,1,2],[0,1,2]", 
            'shots': 1000,
            'qubits': 10,
            'selected_server': 0,
            'eyegod': 'false',
            'eyeqt': 'false',
            'remi': 'false',
            'remifile': ''
        }

    return requests.post("http://q.iphy.ac.cn/scq_submit_task.php", data=request_body)