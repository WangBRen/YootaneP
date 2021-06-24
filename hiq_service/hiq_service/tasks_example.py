from celery import Celery, result
from celery.result import AsyncResult
import sys
sys.path.append('./project')

#安装rabbitmq 本地rabbitmq连接
CELERY_BROKER_URL = 'amqp://myuser:mypassword@localhost:5672/myvhost'
#安装redis 本地redis连接
CELERY_RESULT_BACKEND = 'redis://localhost'

app = Celery('tasks', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND, include=['project.tasks'])

#业务代码
@app.task()
def operation(data):
    result = data
    return result

def add(a, b):
    result = a + b
    return result


#启动worker：celery -A project.tasks worker --loglevel=DEBUG -c=1进程数

#例子
#调用operation，可以在任何位置，例如接http request
result = operation.delay(1)
result.id 

#getResult
getResult = AsyncResult(result.id, app=app)
result.state #任务状态
result.ready() #任务是否执行完毕
result.get() #任务结果
result.traceback # 失败后的回溯追踪

result = add.delay(1, 2)
print(result.id)



