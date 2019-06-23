FROM node:12.4-alpine AS event_service_common
WORKDIR /usr/src/app/event_service
COPY ./package.json ./

FROM event_service_common AS event_service_dev
RUN yarn install