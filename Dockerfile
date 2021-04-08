FROM python:3.7-slim

RUN pip3 install wait-for-dep[websockets,rabbitmq,memcached,mysql,postgres,kafka,redis,mongodb]==0.3.0

ENTRYPOINT ["wait-for-dep"]
