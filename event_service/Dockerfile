FROM node:13.10.1-alpine AS event_service_common
ENV NODE_PATH=/usr/src/app/.service_modules/node_modules
ENV PATH=/usr/src/app/.service_modules/node_modules/.bin:$PATH
WORKDIR /usr/src/app/.service_modules
COPY ./package.json ./
COPY ./yarn.lock ./

FROM event_service_common AS event_service_dev
RUN yarn install
WORKDIR /usr/src/app/event_service

FROM event_service_common AS event_service_prod
WORKDIR /usr/src/app/event_service
COPY . ./
WORKDIR /usr/src/app/.service_modules
RUN yarn install --production && yarn cache clean
WORKDIR /usr/src/app/event_service
RUN yarn run build