ARG BUILD_ENV=dev

FROM node:11.3 AS clipboard_site_dependencies
WORKDIR /usr/src/app/clipboard_site
COPY package.json ./
RUN npm install

FROM clipboard_site_dependencies AS clipboard_site_dev
COPY . ./

FROM clipboard_site_dev AS clipboard_site_prod
RUN npm run build