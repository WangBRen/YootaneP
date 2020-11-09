FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.worker.txt ./
# RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --no-cache-dir -r requirements.worker.txt
RUN pip install -r requirements.worker.txt

COPY . .

# CMD celery worker hiq_service.tasks --loglevel=DEBUG
CMD celery -A hiq_service.tasks worker --loglevel=DEBUG
# CMD python manage.py migrate djcelery
# CMD python manage.py celery worker -c 4 --loglevel=info
