FROM python:3.7-slim

RUN pip3 install wait-for-dep[websockets,rabbitmq,memcached,mysql,postgres,kafka,redis]

ENTRYPOINT ["wait-for-dep"]
