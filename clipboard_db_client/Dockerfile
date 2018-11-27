FROM node:11.2 AS clipboard_db_client
WORKDIR /usr/src/app/clipboard_db_client
COPY ./clipboard_db_client/package.json ./
RUN npm install

FROM clipboard_db_client
COPY ./clipboard_db_client ./
ENTRYPOINT ["npm", "run", "debug"]