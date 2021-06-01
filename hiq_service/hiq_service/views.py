from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from celery.result import AsyncResult

from hiq_service.tasks import ask
from hiq_service.tasks import app
from hiq_service.Task import get_task_list, create_task
from IOPTest import getResult
import json

@api_view(['POST'])
def question(request):
    result = ask.delay(request.data)
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

    
