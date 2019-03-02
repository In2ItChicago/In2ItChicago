FROM nginx:1.15.8 AS nginx_common

FROM nginx_common as nginx_dev
WORKDIR /etc/nginx
RUN apt-get update
RUN apt-get install -yq gnupg
COPY ./install-npm.sh ./
COPY package.json ./
RUN chmod +x install-npm.sh
RUN ./install-npm.sh
RUN npm install

COPY ./requirements.txt ./
RUN apt-get install -yq python3
RUN apt-get install -yq python3-pip
RUN pip3 install -r requirements.txt