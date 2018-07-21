FROM alpine:edge
COPY * /app/
WORKDIR /app
RUN apk add --no-cache python3 \
    python3-dev \
    build-base \
    git && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt && \
    apk del python3-dev \
    build-base \
    git && \
    rm -r /root/.cache
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--worker-class", "sanic.worker.GunicornWorker", "--preload"]
