FROM node:11.6 AS event_service_common
WORKDIR /usr/src/app/event_service
COPY ./package.json ./

FROM event_service_common
RUN npm install