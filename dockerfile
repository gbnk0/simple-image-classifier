FROM debian:stretch-slim

COPY ./app/ /app/

WORKDIR /app

RUN apt-get update && apt-get -y install python3 python3-pip python3-setuptools && \
    pip3 install -r requirements.txt && \
    apt-get autoremove python3-pip -y && \
    apt-get -y clean && apt-get -y autoremove

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--worker-class", "sanic.worker.GunicornWorker", "--preload"]
