FROM python:3.7.2 AS event_processor_common
WORKDIR /usr/src/app/event_processor
RUN pip3 install -U pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

FROM event_processor_common AS event_processor_prod
COPY . ./