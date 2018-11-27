FROM node:11.2 AS clipboard_site
WORKDIR /usr/src/app/clipboard_site
COPY ./clipboard_site/package.json ./
RUN npm install

FROM clipboard_site
COPY ./clipboard_site ./
ENTRYPOINT ["npm", "run", "docker-debug"]