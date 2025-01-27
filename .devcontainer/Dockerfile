FROM python:3.11-slim

# プロキシ設定用の引数
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY

# プロキシ環境変数の設定
ENV HTTP_PROXY=${HTTP_PROXY} \
    HTTPS_PROXY=${HTTPS_PROXY} \
    NO_PROXY=${NO_PROXY} \
    http_proxy=${HTTP_PROXY} \
    https_proxy=${HTTPS_PROXY} \
    no_proxy=${NO_PROXY}

WORKDIR /workspace

RUN apt update && \
    apt install -y git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*