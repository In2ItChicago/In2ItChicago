FROM node:11.9 AS in2it_site_common
WORKDIR /usr/src/app/in2it_site
COPY package.json ./

FROM in2it_site_common AS in2it_site_prod
COPY . ./
RUN npm install --production
RUN npm run build