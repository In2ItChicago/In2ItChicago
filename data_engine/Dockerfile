FROM python:3.6.6

WORKDIR /dataengine
COPY . /dataengine/

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "runner.py"]
