import json
from peewee import *
import time 
import datetime

settings = {'host': '139.159.177.11', 'password': 'password', 'port': 3306, 'user': 'root'}
db = MySQLDatabase('HiQASM', **settings)

class BaseModel(Model):
    class Meta:
        database = db


#task 包含的所有参数
class Task(BaseModel):
    command = TextField()
    state = CharField()
    log = TextField()
    result = TextField()
    time_use = FloatField()
    inserted_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    started = DateTimeField(null=True)
    finished = DateTimeField(null=True)


# 提交一个新任务
#  task = get_task_earliest(这里传入任务执行的命令)
def create_task(command):
    print("create_task")
    time = datetime.datetime.now()
    task = Task.create(command = command,state = 'pending',inserted_at = time, updated_at = time)
    return task

# 获取指定id任务结果
# task = get_task(想要获取的任务的id)
# 打印该任务的id和命令
# print(task.id, task.command)
def get_task(task_id):
    tasks = Task.select().where(Task.id==task_id).limit(1)
    return tasks[0]

# 获取所有任务
# 返回值是一个list
# 若 tasks = get_tasks_all()
# 想获取第一个任务
# task = tasks[0]
# 打印该任务的id和命令 其他参数可见Task model
# print(task.id, task.command)
def get_tasks_all():
    tasks = Task.select()
    return tasks

# 获取所有等待中任务
# 返回值是一个list
# 若 tasks = get_tasks_unfinished()
# 想获取第一个任务
# task = tasks[0]
# 打印该任务的id和命令 其他参数可见Task model
# print(task.id, task.command)
def get_tasks_unfinished():
    tasks = Task.select().where(Task.state == "pending")
    return tasks

# 获取最早提交的任务 返回结果为一个任务对象 
# task = get_task_earliest()
# print(task.id, task.command)
def get_task_earliest():
    tasks = Task.select().where(Task.state == "pending").order_by(Task.inserted_at).limit(1)
    return tasks[0]

# 变更任务状态为开始试验
# 参数为任务id
def change_task_state(task_id):
    time = datetime.datetime.now()
    task = Task.update(state = "running", updated_at = time, started = time).where(Task.id==task_id).execute()
    return task

# 结束任务，提交结果，log为缺省值
def finish_task(task_id, result, log=''):
    time = datetime.datetime.now()
    task = Task.update(state = "success", result = result, finished = time, updated_at = time).where(Task.id==task_id).execute()
    return task

# 结束失败任务，提交log缺省值
def fail_task(task_id, log=''):
    time = datetime.datetime.now()
    task = Task.update(state = "fail", log = log, finished = time, updated_at = time).where(Task.id==task_id).execute()
    return task

def get_task_list(page, size):
    try:
        find = Task.select().order_by(Task.inserted_at).paginate(int(page), int(size))
        index = 0
        list = []
        while index < len(find):
            print(find[index].command)
            list.append(
                {'id': find[index].id, 'command': find[index].command, 'state': find[index].state, 'log': find[index].log, 'result': find[index].result,
                 'time_use': find[index].time_use, 'inserted_at': find[index].inserted_at, 'updated_at': find[index].updated_at, 'started': find[index].started, 'finished': find[index].finished})
            index += 1
        return list
    except:
        return []