FROM node:12.1-alpine AS event_service_common
WORKDIR /usr/src/app/event_service
COPY ./package.json ./

FROM event_service_common AS event_service_prod
COPY . ./
RUN yarn install --production
RUN yarn run build