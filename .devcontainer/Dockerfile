FROM python:3.11-slim

WORKDIR /workspace

RUN apt update && \
    apt install -y git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*