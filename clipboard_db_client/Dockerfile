FROM node:11.6 AS clipboard_db_client_deps
WORKDIR /usr/src/app/clipboard_db_client
COPY ./package.json ./
RUN npm install

FROM clipboard_db_client_deps
COPY . ./