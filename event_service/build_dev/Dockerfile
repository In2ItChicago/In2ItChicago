FROM node:12.8.1-alpine AS event_service_common
WORKDIR /data/
COPY ./package.json ./
#COPY ./yarn.lock ./

FROM event_service_common AS event_service_dev
RUN yarn install
ENV NODE_PATH=/data/node_modules
ENV PATH=/data/node_modules/.bin:$PATH
WORKDIR /usr/src/app/event_service
