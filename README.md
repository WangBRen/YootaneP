# 本地开发环境

## 准备工作

- Install docker and docker-compose for your environment
  - https://docs.docker.com/compose/install/#install-compose
- Check the versions and make sure they are no errors

    ```shell
    docker version
    docker-compose version
    ```

## 步骤

- Clone this repo
- Rename file `dev.env` to `.env`

    ```shell
    cp dev.env .env
    ```
    
- Open `.env` and edit the environment variable values accordingly

    ```bash
    ENV=dev
    
	# docker
	DOCKER_REGISTRY_URL=localhost:5000
	DOCKER_PROJECT=hiq/hiq-master
    
    # rabbitmq
    RABBITMQ_DEFAULT_USER=admin # rabbitmq admin username
    RABBITMQ_DEFAULT_PASS=HiqControl # rabbitmq admin password
    RABBITMQ_DATA_DIR=<rabbitmq local data directory> # i.e. "/var/lib/hiq-master/data/rabbitmq"
    
    # redis
    REDIS_DATA_DIR=<redis local data directory> # i.e. "/var/lib/hiq-master/data/redis"
    
    # celery
    CELERY_BROKER_URL=pyamqp://guest:guest@hiq-rabbitmq// # rabbitmq connection string
    CELERY_RESULT_BACKEND=redis://hiq-redis # redis connection string
    ```

- Start up the services 

    ```text
    docker-compose up --build
    ```
    This may take a while the first time as docker is downloading all images to your computer and building some locally
    
- Create RabbitMQ user (First time only)
    - Visit RabbitMQ management portal http://127.0.0.1:15672
    - Create the user you specified in the `.env` file `CELERY_BROKER_URL` field
	- Set appropriate permissions for this user
    - Start services
    
    ```text
    docker-compose up --build
    ```

- Sprint Boot Swagger-UI should now be ready
    - https://127.0.0.1/swagger-ui.html

## 各个后台入口

|入口|地址|用户名|密码|
|-|-|-|-|
|Sprint Boot Swagger UI|https://127.0.0.1/swagger-ui.html|无|无|
|RabbitMQ 队列服务|http://127.0.0.1:15672|`admin`|`HiqControl`|
|Redis 键值数据库|http://127.0.0.1:8081|无|无|

