FROM node:11.2 AS clipboard_db_client_deps
WORKDIR /usr/src/app/clipboard_db_client
COPY ./package.json ./
RUN npm install

FROM clipboard_db_client_deps
COPY . ./
ENTRYPOINT ["npm", "run", "debug"]