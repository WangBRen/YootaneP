from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from celery.result import AsyncResult

from hiq_service.tasks import ask
from hiq_service.tasks import app

@api_view(['POST'])
def question(request):
    result = ask.delay(request.data)
    return Response(result.id, status=status.HTTP_202_ACCEPTED)


@api_view(['GET'])
def answer(request, pk):
    result = AsyncResult(pk, app=app)

    if result.ready():
        return Response(result.get(), status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
    else:
        return Response(result.state, status=status.HTTP_200_OK, content_type='application/json; charset=utf-8')
        # return Response(result.state, status=status.HTTP_404_NOT_FOUND, content_type='application/json; charset=utf-8')

