import os
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from yt_service.ecg import ecg
from yt_service.predict_func import predict_func


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

@api_view(['POST'])
def predict(request):
    data=request.data
    result = predict_func(data)
    
    return Response(result, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
#    return HttpResponse(result, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
