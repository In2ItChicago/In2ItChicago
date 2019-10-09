FROM python:3.7.3-alpine AS event_processor_common
WORKDIR /data/
COPY Pipfile ./
#COPY Pipfile.lock ./
RUN pip3 install -U pip && apk update && apk add --no-cache libxslt libstdc++ && \
    apk add --no-cache --virtual .build-deps gcc git \
    musl-dev libffi-dev \
    openssl-dev libxml2-dev libxslt-dev g++ && \
    pip3 install pipenv && \
    pipenv lock --verbose && \
    pipenv install --system --dev --verbose && \
    apk --purge del .build-deps

FROM event_processor_common AS event_processor_dev
WORKDIR /data/
COPY package.json ./
RUN apk add nodejs-npm && npm install
ENV PATH /data/node_modules/.bin:$PATH
WORKDIR /usr/src/app/event_processor
