ARG BUILD_ENV=dev

FROM node:11.6 AS in2it_site_deps
WORKDIR /usr/src/app/in2it_site
COPY package.json ./
RUN npm install

FROM in2it_site_deps AS in2it_site_dev
COPY . ./

FROM in2it_site_dev AS in2it_site_prod
RUN npm run build