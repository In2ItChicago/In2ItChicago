FROM nginx:1.15.9 AS nginx_common

FROM nginx_common as nginx_dev
WORKDIR /etc/nginx
RUN apt-get update
RUN apt-get install -yq gnupg
RUN apk update
RUN apk add nodejs-npm
RUN npm install -g nodemon

COPY ./requirements.txt ./
RUN apt-get install -yq python3
RUN apt-get install -yq python3-pip
RUN pip3 install -r requirements.txt