FROM python:latest

WORKDIR /dataengine
ADD ./*.py /dataengine/
ADD data_aggregators /dataengine/data_aggregators
ADD ./requirements.txt /dataengine

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "runner.py"]
