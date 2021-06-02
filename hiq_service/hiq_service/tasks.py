from celery import Celery, result
import time
import os
import sys
sys.path.append('./hiq_service')
import socket
import zhinst.ziPython
from iop import getResult

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', '')

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['hiq_service.tasks'])

@app.task()
def ask(data):
    #操作并处理结果
    print(data)
    dev = 'dev8276'
    d = zhinst.ziPython.ziDiscovery()
    props = d.get(d.find(dev))
    return props

@app.task()
def ask_iop(data):
    #iop任务提交
    print(data)
    result=getResult(data)
    return result

