FROM node:11.6 AS event_service_common
WORKDIR /usr/src/app/event_service
COPY ./package.json ./

FROM event_service_common AS event_service_prod
COPY . ./
RUN npm install --production