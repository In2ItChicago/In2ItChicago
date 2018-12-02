FROM node:11.2 AS clipboard_site_deps
WORKDIR /usr/src/app/clipboard_site
COPY package.json ./
RUN npm install

FROM clipboard_site_deps
COPY . ./
#ENTRYPOINT [ "sh", "-c", "sleep infinity" ]
ENTRYPOINT ["npm", "run", "docker-debug"]