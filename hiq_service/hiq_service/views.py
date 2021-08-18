import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from celery.result import AsyncResult

from hiq_service.tasks import ask, ask_iop, execute
from hiq_service.tasks import app
from hiq_service.Task import get_task_list, create_task
from iop import getResult
import json

from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser

##上传代码文件接口
class FileUploadView(APIView):
    parser_classes = [FileUploadParser, ]

    def put(self, request, filename, format=None):
        #获取文件
        file_obj = request.data['file']
        #调用文件处理排队
        result = execute.delay(file_obj, filename)
        #返回任务id
        return Response(result.id, status=status.HTTP_202_ACCEPTED)

##通过id获取结果
@api_view(['GET'])
def result(request, pk):
    result = AsyncResult(pk, app=app)

    if result.ready():
        return Response(result.get(), status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
    else:
        return Response(result.state, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        # return Response(result.state, status=status.HTTP_404_NOT_FOUND, content_type='application/json; charset=utf-8')

@api_view(['POST'])
def question(request):
    result = ask.delay(request.data)
    return Response(result.id, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def question_iop(request):
    result = ask_iop.delay(request.data)
    return Response(result.id, status=status.HTTP_202_ACCEPTED)

@api_view(['POST'])
def iop(request):
    result = getResult(request.data)
    return Response(result, status=status.HTTP_200_OK)

@api_view(['GET'])
def answer(request, pk):
    result = AsyncResult(pk, app=app)

    if result.ready():
        return Response(result.get(), status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
    else:
        return Response(result.state, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        # return Response(result.state, status=status.HTTP_404_NOT_FOUND, content_type='application/json; charset=utf-8')

@api_view(['GET'])
def answer_iop(request, pk):
    result = AsyncResult(pk, app=app)

    if result.ready():
        return Response(result.get(), status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
    else:
        return Response(result.state, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        # return Response(result.state, status=status.HTTP_404_NOT_FOUND, content_type='application/json; charset=utf-8')

@api_view(['GET'])
def path(request):
    root = os.getcwd()
    result = os.walk("/")
    print(root)
    print(result)
    return Response(result, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')



@api_view(['POST'])
def task(request):
    print("create_task")
    print(request.data["command"])
    result = create_task(request.data["command"])
    return Response(result.id, status=status.HTTP_202_ACCEPTED)

@api_view(['GET'])
def get_task(request):
    try:
        task_list = get_task_list(request.GET.get("page"), request.GET.get("size"))
        data = json.dumps({
                        'page': request.GET.get("page"),
                        'size': request.GET.get("size"),
                        'data': []
                    })
       
    except:
        task_list = get_task_list(1, 20)
        data = json.dumps({
                'page': 1,
                'size': 20,
                'data': []
            })
    return Response(data, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

    
