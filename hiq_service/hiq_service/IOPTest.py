import requests

def trans_iop_a(self):
    op_list = self["blocks"]
    n=len(op_list)
    last_iop = []
    mea = []
    hiq_list=[[[] for col in range(10)] for row in range(10)]
    for k in range(n-1):
        for i in range(n-1-k):
            if op_list[i]['pos'][0]>op_list[i+1]['pos'][0]:
                op_list[i],op_list[i+1] = op_list[i+1],op_list[i]
    
    r=[0]*10
    op0 = []
    op1 = []
    op2 = []

    for i in range(n):
            k = op_list[i]['pos'][0]
            j = op_list[i]['pos'][1]
            hiq_list[k][j] = op_list[i]['type']           

            
            if  j == 0:
                op = hiq_list[k][j]
                if op == 'Measure':
                    mea.append(j)
                op_0 = []
                op_0.append(op.lower())
                op_0.append(j)
                if op_list[i]['ctrls'] == []:
                    para = 0
                else: 
                    para = op_list[i]['ctrls'][0]
                    
                op_0.append(para)
                r[0] += 1
                if r[0] <= 1:
                    last_iop.append(j) 
                op_h = []
                op_h = op_0
                  
            if  j == 1:
                op = hiq_list[k][j]
                if op == 'Measure':
                    mea.append(j)
                op_1 = []
                op_1.append(op.lower())
                op_1.append(j)
                if op_list[i]['ctrls'] == []:
                    para = 0
                else: 
                    para = op_list[i]['ctrls'][0]
                op_1.append(para)
                
                r[1] += 1
                
                if r[1] <= 1:
                    last_iop.append(j) 
                op_h = []
                op_h = op_1
            
            if  j == 2:
                op = hiq_list[k][j]
                if op == 'Measure':
                    mea.append(j)
                op_2 = []
                op_2.append(op.lower())
                op_2.append(j)
                if op_list[i]['ctrls'] == []:
                    para = 0
                else: 
                    para = op_list[i]['ctrls'][0]
                
                op_2.append(para)
                
                r[2] += 1
                if r[2] <= 1:
                    last_iop.append(j) 
                op_h = []
                op_h = op_2
                
                    
            if k == 0:
                op0.append(op_h)
            if k == 1:
                op1.append(op_h)
            if k == 2:
                op2.append(op_h)
                    
            
    return  op0,op1,op2,mea,last_iop

def getResult(data):
    print(data)
    body = trans_iop_a(data)
    print(body)
    # return body
    request_body = {
            'qtasm': "[[\\'H\\',0,0]],[0],[0]",
            # 'qtasm': body,
            'shots': 1000,
            'qubits': 10,
            'selected_server': 0,
            'eyegod': 'false',
            'eyeqt': 'false',
            'remi': 'false',
            'remifile': ''
        }

    return requests.post("http://q.iphy.ac.cn/test2.php", data=request_body)