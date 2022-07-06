FROM python:latest

ADD main.py /validator/

WORKDIR /validator/

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379
ENV REDIS_SUBSCRIBE_KEY=message_to_approve
ENV REDIS_APPROVED_PUBLISH_KEY=approved_messages
ENV REDIS_UNAPPROVED_PUBLISH_KEY=unapproved_messages

RUN pip3 install redis
CMD python3 main.py