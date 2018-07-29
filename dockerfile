FROM debian:stretch-slim
ARG VCS_REF
LABEL org.label-schema.vcs-ref=$VCS_REF \
        org.label-schema.vcs-url="https://github.com/gbnk0/simple-image-classifier"

COPY ./app/ /app/

WORKDIR /app

RUN apt-get update && apt-get -y install python3 python3-pip && \
    pip3 install -r requirements.txt && apt-get -y clean && apt-get -y autoremove

EXPOSE 8080

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--worker-class", "sanic.worker.GunicornWorker", "--preload"]
