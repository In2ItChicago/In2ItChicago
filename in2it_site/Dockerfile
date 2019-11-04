FROM node:12.8.1-alpine AS in2it_site_common
WORKDIR /usr/src/app/.service_modules
COPY ./package.json ./
#COPY ./.yarnrc ./
COPY ./yarn.lock ./

FROM in2it_site_common AS in2it_site_dev
RUN yarn install --verbose
ENV NODE_PATH=/usr/src/app/.service_modules/node_modules
ENV PATH=/usr/src/app/app/.service_modules/node_modules/.bin:$PATH
WORKDIR /usr/src/app/in2it_site

FROM in2it_site_common AS in2it_site_prod
COPY . ./
RUN yarn install --production --verbose && yarn cache clean && yarn run build