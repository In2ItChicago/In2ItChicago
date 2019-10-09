FROM node:12.8.1-alpine AS in2it_site_common
WORKDIR /data
COPY package.json ./
#COPY yarn.lock ./

FROM in2it_site_common AS in2it_site_dev
RUN yarn install
ENV NODE_PATH=/data/node_modules
ENV PATH=/data/node_modules/.bin:$PATH
WORKDIR /usr/src/app/in2it_site
