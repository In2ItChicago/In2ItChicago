FROM node:12.8.1-alpine AS event_service_common
WORKDIR /usr/src/app/event_service
COPY ./package.json ./
COPY ./yarn.lock ./

FROM event_service_common AS event_service_prod
COPY . ./
RUN yarn install --production && yarn cache clean && yarn run build
