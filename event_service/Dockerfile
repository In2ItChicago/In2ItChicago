FROM node:11.6 AS event_service_deps
WORKDIR /usr/src/app/event_service
COPY ./package.json ./
RUN npm install

FROM event_service_deps
COPY . ./