FROM python:latest

ADD main.py /validator/

WORKDIR /validator/

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_SUBSCRIBE_KEY=*

RUN pip3 install redis
RUN python3 main.py