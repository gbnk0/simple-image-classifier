FROM debian:stretch
COPY * /app/
WORKDIR /app
ENV HTTP_PROXY="http://127.0.0.1:3128"
ENV HTTPS_PROXY="http://127.0.0.1:3128"
RUN apt-get update && apt-get -y install python3 python3-pip && \
    pip3 install tensorflow>=1.9.0 && \
    pip3 install -r requirements.txt && \
    apt-get -y clean && apt-get -y autoremove
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--worker-class", "sanic.worker.GunicornWorker", "--preload"]
