# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 21:59:54 2022

@author: 24425
"""
import json
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve,auc
import matplotlib.pyplot as plt
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.utils.class_weight import compute_class_weight
from sklearn.externals import joblib
import numpy as np
std_new_patient_list=[]
std_old_patient_list=[]
model_new_patient_list=[]
model_old_patient_list=[]
for i in range(1,9):
    std=joblib.load('./std_0_'+str(i))
    std_new_patient_list.append(std)
    
    std=joblib.load('./std_1_'+str(i))
    std_old_patient_list.append(std)
    
    model=joblib.load('./model_0_'+str(i))
    model_new_patient_list.append(model)
    
    model=joblib.load('./model_1_'+str(i))
    model_old_patient_list.append(model)


def predict_func(data):

    is_new_patient=data["is_new_patient"]
    standard=data["standard"]
    personal_data=data["personal_data"]
    BEFORE_SBP=personal_data['BEFORE_SBP']
    BEFORE_DBP=personal_data['BEFORE_DBP']
    BEFORE_WEIGHT=personal_data['BEFORE_WEIGHT']
    DRY_WEIGHT=personal_data['DRY_WEIGHT']
    each_x= [BEFORE_SBP,BEFORE_DBP,
             BEFORE_WEIGHT,DRY_WEIGHT,
             BEFORE_WEIGHT-DRY_WEIGHT]
    if is_new_patient:
        '''
        e.g. X=[120.  80.  90.  86.   4.  37.   4.   1.] Y=1
        '''
        stdsc=std_new_patient_list[standard-1]
        model=model_new_patient_list[standard-1]
    else:
        '''
        e.g. X=[114.,77.,89.,86.,3.,143.33333333,6.01849003,7.,4.,-7.
,4.,88.33333333,3.77123617,4.,4.,-4.,4.,106.66666667,4.49691252,1.
,0.,1.,37.,4.,1.,] Y=1
        '''
        
        stdsc=std_old_patient_list[standard-1]
        model=model_old_patient_list[standard-1]

        
        SBP_mean=personal_data['SBP_mean']
        SBP_std=personal_data['SBP_std']
        SBP_diff_abs_mean=personal_data['SBP_diff_abs_mean']
        SBP_diff_abs_std=personal_data['SBP_diff_abs_std']
        SBP_diff_mean=personal_data['SBP_diff_mean']
        SBP_diff_std=personal_data['SBP_diff_std']
        DBP_mean=personal_data['DBP_mean']
        DBP_std=personal_data['DBP_std']
        DBP_diff_abs_mean=personal_data['DBP_diff_abs_mean']
        DBP_diff_abs_std=personal_data['DBP_diff_abs_std']
        DBP_diff_mean=personal_data['DBP_diff_mean']
        DBP_diff_std=personal_data['DBP_diff_std']
        MEAN_AP_mean=personal_data['MEAN_AP_mean']
        MEAN_AP_std=personal_data['MEAN_AP_std']
        UFV_max=personal_data['UFV_max']
        UFR_max=personal_data['UFR_max']
        history_LBP_rate=personal_data['history_LBP_rate']
        each_x=each_x+[SBP_mean,SBP_std,
                          SBP_diff_abs_mean,SBP_diff_abs_std,
                          SBP_diff_mean,SBP_diff_std,
                          DBP_mean,DBP_std,
                          DBP_diff_abs_mean,DBP_diff_abs_std,
                          DBP_diff_mean,DBP_diff_std,
                          MEAN_AP_mean,MEAN_AP_std,
                          UFV_max,UFR_max,history_LBP_rate]
    
    AGE=personal_data['AGE']
    DIALYSIS_DURATION=personal_data['DIALYSIS_DURATION']
    each_x=each_x+[AGE,DIALYSIS_DURATION]
    GENDER=personal_data['GENDER']

    if GENDER==1:
        each_x=each_x+[1]
    else:
        each_x=each_x+[0]
    
    each_x=np.array([each_x])
    stdsc=StandardScaler().fit(each_x[:,:-1])#正态分布标准化数据的函数
    X_std=stdsc.fit_transform(each_x[:,:-1])
    X_std = np.concatenate((X_std,each_x[:,-1:]),axis=1)
    
    if not is_new_patient:
        X_std[:,-4]=each_x[:,-4]
    predictions=model.predict_proba(X_std)
    result={'result':predictions[0,1]}
    result = json.dumps(result, ensure_ascii=False)
    return result
if __name__ == '__main__':
    
#    a=[120,80,90,86,4,37,4,1,]
    BEFORE_SBP,BEFORE_DBP,BEFORE_WEIGHT,DRY_WEIGHT=120,80,90,86
    AGE,DIALYSIS_DURATION,GENDER=37,4,1
    data={'is_new_patient':True,
          'standard':0,
          'personal_data':
              {'BEFORE_SBP':BEFORE_SBP,
               'BEFORE_DBP':BEFORE_DBP,
               'BEFORE_WEIGHT':BEFORE_WEIGHT,
               'DRY_WEIGHT':DRY_WEIGHT,
               'AGE':AGE,
               'DIALYSIS_DURATION':DIALYSIS_DURATION,
               'GENDER':GENDER,}
          }
    result=predict_func(data)
    '''
    X=[114.,77.,89.,86.,3.,143.33333333,6.01849003,7.,4.,-7.
,4.,88.33333333,3.77123617,4.,4.,-4.,4.,106.66666667,4.49691252,1.
,0.,1.,37.,4.,1.,] Y=1
    '''
    BEFORE_SBP,BEFORE_DBP,BEFORE_WEIGHT,DRY_WEIGHT=114.,77.,89.,86
    
    SBP_mean,SBP_std,=143.33333333,6.01849003,
    SBP_diff_abs_mean,SBP_diff_abs_std=7.,4.
    SBP_diff_mean,SBP_diff_std=-7.,4
    DBP_mean,DBP_std,=88.33333333,3.77123617,
    DBP_diff_abs_mean,DBP_diff_abs_std=4.,4
    DBP_diff_mean,DBP_diff_std=4.,4.
    MEAN_AP_mean,MEAN_AP_std=106.66666667,4.49691252,
    UFV_max,UFR_max,history_LBP_rate=1.,0.,1.
    
    
    AGE,DIALYSIS_DURATION,GENDER=37,4,1
    data={'is_new_patient':False,
          'standard':0,
          'personal_data':
              {'BEFORE_SBP':BEFORE_SBP,
               'BEFORE_DBP':BEFORE_DBP,
               'BEFORE_WEIGHT':BEFORE_WEIGHT,
               'DRY_WEIGHT':DRY_WEIGHT,
               
               'SBP_mean':SBP_mean,
               'SBP_std':SBP_std,
               'SBP_diff_abs_mean':SBP_diff_abs_mean,
               'SBP_diff_abs_std':SBP_diff_abs_std,
               'SBP_diff_mean':SBP_diff_mean,
               'SBP_diff_std':SBP_diff_std,
               'DBP_mean':DBP_mean,
               'DBP_std':DBP_std,
               'DBP_diff_abs_mean':DBP_diff_abs_mean,
               'DBP_diff_abs_std':DBP_diff_abs_std,
               'DBP_diff_mean':DBP_diff_mean,
               'DBP_diff_std':DBP_diff_std,
               'MEAN_AP_mean':MEAN_AP_mean,
               'MEAN_AP_std':MEAN_AP_std,
               'UFV_max':UFV_max,
               'UFR_max':UFR_max,
               'history_LBP_rate':history_LBP_rate,
               
               'AGE':AGE,
               'DIALYSIS_DURATION':DIALYSIS_DURATION,
               'GENDER':GENDER,}
          
          }
    result=predict_func(data)
    data = json.dumps(data, ensure_ascii=False)
