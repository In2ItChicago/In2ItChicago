FROM python:3.7.3-alpine AS event_processor_common
WORKDIR /usr/src/app/event_processor
COPY requirements.txt ./
RUN pip3 install -U pip && apk update && apk add libxslt && apk add --no-cache \
    --virtual .build-deps gcc musl-dev libffi-dev \
    openssl-dev libxml2-dev libxslt-dev g++ && \
    pip3 install -r requirements.txt && \
    apk --purge del .build-deps

FROM event_processor_common AS event_processor_dev
COPY package.json ./
RUN apk add nodejs-npm && npm install