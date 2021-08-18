"""hiq_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.urls import re_path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from hiq_service import views

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^question/$', views.question),
    url(r'^question_iop/$', views.question_iop),
    url(r'^iop/$', views.iop),
    url(r'^question/(?P<pk>[a-zA-Z0-9]{8}-([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12})/$', views.answer),
    url(r'^question_iop/(?P<pk>[a-zA-Z0-9]{8}-([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12})/$', views.answer_iop),
    url(r'^task/$', views.task),
    url(r'^tasks', views.get_task),
    #/上传接口的 URL 为 http://xx.xx.xx.xx/files/<filename> ，其中 <filenmae> 用于指定上传成功后在服务器端的文件名。使用 PUT 请求上传文件。
    re_path(r'^files/(?P<filename>[^/]+)$', views.FileUploadView.as_view()),
    url(r'^result/(?P<pk>[a-zA-Z0-9]{8}-([a-zA-Z0-9]{4}-){3}[a-zA-Z0-9]{12})/$', views.result),
    url(r'^path/', views.path),
]

urlpatterns = format_suffix_patterns(urlpatterns)
