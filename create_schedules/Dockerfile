FROM python:3.8.2-alpine
ARG BUILD_ENV
WORKDIR /app
COPY . .
RUN pip3 install -U pip && apk update && \
    pip3 install requests

