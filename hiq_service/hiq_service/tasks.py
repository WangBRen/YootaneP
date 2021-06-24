from celery import Celery, result
import time
import os
import sys
sys.path.append('./hiq_service')
import socket
from iop import getResult

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', '')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', '')

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['hiq_service.tasks'])

@app.task()
def ask(data):
    #操作并处理结果
    print(data)
    return data


@app.task()
def execute(file_obj, filename):
    #对文件进行操作
    with open(filename, 'wb') as f:
        for chunk in file_obj.chunks():
            f.write(chunk)
    return filename

@app.task()
def ask_iop(data):
    #iop任务提交
    print(data)
    result=getResult(data)
    return result

