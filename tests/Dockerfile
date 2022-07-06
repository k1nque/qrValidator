FROM redis:alpine
ADD tests.py /tests/
WORKDIR /tests/
RUN apk add bash
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install redis
#CMD python3 test.py