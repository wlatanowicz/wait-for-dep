FROM python:3.7-slim

RUN pip3 install wait-for-dep[websockets,rabbitmq,memcached,mysql,postgres,kafka,redis]==0.2.1

ENTRYPOINT ["wait-for-dep"]
