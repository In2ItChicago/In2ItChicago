FROM python:3.7.2
WORKDIR /usr/src/app/event_processor
RUN pip3 install -U pip
COPY requirements.txt ./
COPY install-npm.sh ./
COPY package.json ./
RUN chmod +x install-npm.sh
RUN pip3 install -r requirements.txt
RUN ./install-npm.sh
RUN npm install