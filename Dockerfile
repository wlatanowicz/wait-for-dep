FROM python:3.7-slim

COPY wait_for_dep /wait-for-dep/wait_for_dep/
COPY requirements /wait-for-dep/requirements/
COPY setup.py /wait-for-dep/setup.py

RUN pip3 install -e /wait-for-dep[websockets,rabbitmq,memcached,mysql,postgres,kafka,redis]

ENTRYPOINT ["wait-for-dep"]
