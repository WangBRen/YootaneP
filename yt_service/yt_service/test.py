# Load NeuroKit and other useful packages
import numpy as np
import pandas as pd
import neurokit2 as nk

dataset = pd.read_csv(r"/Users/cht/Downloads/Myocardial-Ischemia-Detection-by-Analysing-ECG-Signal-master/Dataset/工作簿3.csv",)#read data 
#Calculate moving average with 0.75s in both directions, then append do dataset

ecg_signal = nk.ecg_clean(dataset,method='neurokit')
# Extract R-peaks locations

_, rpeaks = nk.ecg_peaks(ecg_signal, sampling_rate=500,method="neurokit")

# Delineate the ECG signal
signal_cwt, waves_cwt = nk.ecg_delineate(ecg_signal, sampling_rate=500, method="cwt", show=False)
