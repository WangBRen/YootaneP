FROM python:3.7

# install required packages
# RUN apt-get update && \
#     apt-get install -y nginx && \
#     apt-get install -y supervisor
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U setuptools

# install uwsgi
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple uwsgi

# configure nginx, disable daemon
# RUN echo "daemon off;" >> /etc/nginx/nginx.conf
# RUN mkdir -p /run/nginx

# setup all the configfiles
# COPY nginx-django.conf /etc/nginx/conf.d/
# COPY supervisord-django.conf /etc/supervisor/conf.d/

WORKDIR /usr/src/app
RUN mkdir ./log
COPY . .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.service.txt
# RUN pip install -r requirements.service.txt
EXPOSE 9090

# start it
# CMD /usr/bin/supervisord -n
CMD python3 manage.py runserver 0.0.0.0:9090
