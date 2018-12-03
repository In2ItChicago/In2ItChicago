ARG BUILD_STAGE=compile

FROM node:11.2 AS clipboard_site_dependencies
WORKDIR /usr/src/app/clipboard_site
COPY package.json ./
RUN npm install

FROM clipboard_site_dependencies AS clipboard_site_compile
COPY . ./
RUN npm run build

FROM clipboard_site_${BUILD_STAGE}
CMD ["npm", "run", "docker-debug"]