from celery import Celery
import time
import os
import sys
sys.path.append('./hiq_service')
import socket
import zhinst.ziPython

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

