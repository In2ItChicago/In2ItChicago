FROM python:3.7.3-alpine
WORKDIR /usr/src
COPY . ./
RUN apk add --no-cache postgresql-libs postgresql-client && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt && \
    apk --purge del .build-deps