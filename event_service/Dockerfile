FROM node:12.8.1-alpine AS event_service_common
WORKDIR /usr/src/app/build
COPY ./package.json ./
COPY ./.yarnrc ./
COPY ./yarn.lock ./

FROM event_service_common AS event_service_dev
RUN yarn install --verbose
ENV NODE_PATH=/usr/src/app/service_modules
ENV PATH=/usr/src/app/service_modules/.bin:$PATH
WORKDIR /usr/src/app/event_service

FROM event_service_common AS event_service_prod
COPY . ./
RUN yarn install --production --verbose && yarn cache clean && yarn run build