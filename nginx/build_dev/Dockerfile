FROM nginx:1.15.10 AS nginx_common

FROM nginx_common as nginx_dev
WORKDIR /etc/nginx
COPY ./requirements.txt ./
RUN apt-get update -yq && apt-get upgrade -yq && \
    apt-get install -yq curl && \
    curl -sL https://deb.nodesource.com/setup_10.x | bash - && \
    apt-get install -yq nodejs build-essential && \
    npm install -g npm && \
    npm install -g nodemon && \
    apt-get install -yq python3 && \
    apt-get install -yq python3-pip && \
    pip3 install -r requirements.txt