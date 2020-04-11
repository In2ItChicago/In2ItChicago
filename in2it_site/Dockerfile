FROM node:13.2-alpine AS in2it_site_common
RUN apk add python3 make g++

FROM in2it_site_common AS in2it_site_dev
WORKDIR /usr/src/app/.site_modules
COPY ./package.json ./
COPY ./yarn.lock ./
ENV NODE_PATH=/usr/src/app/.site_modules/node_modules
ENV PATH=/usr/src/app/app/.site_modules/node_modules/.bin:$PATH
RUN yarn install
WORKDIR /usr/src/app/in2it_site

FROM in2it_site_common AS in2it_site_prod
WORKDIR /usr/src/app/in2it_site
COPY . ./
RUN yarn install --production && yarn cache clean && yarn run build && apk --purge del python3 make g++
