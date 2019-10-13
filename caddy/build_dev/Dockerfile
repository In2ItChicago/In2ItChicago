FROM abiosoft/caddy:2.0.0
WORKDIR /srv
COPY ./nodemon.json ./
RUN apk update && apk add nodejs-npm && npm install -g nodemon  