FROM node:11.11 AS in2it_site_common
WORKDIR /usr/src/app/in2it_site
COPY package.json ./

FROM in2it_site_common AS in2it_site_dev
RUN npm install