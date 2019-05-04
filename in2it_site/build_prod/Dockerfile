FROM node:12.1-alpine AS in2it_site_common
WORKDIR /usr/src/app/in2it_site
COPY package.json ./

FROM in2it_site_common AS in2it_site_prod
COPY . ./
RUN yarn install --production
RUN yarn run build