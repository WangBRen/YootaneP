import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from yt_service.ecg import ecg


##上传代码文件接口

@api_view(['GET'])
def path(request):
    return Response('hello', status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

@api_view(['POST'])
def qrs(request):
    data = request.POST.get('data',[])
    result = ecg(data)
    print(result)
    return Response('hello', status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')

