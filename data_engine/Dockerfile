FROM python:3.7

WORKDIR /dataengine
COPY . /dataengine/

# Move this back into requirements.txt when new scrapy version is released
RUN pip3 install git+https://github.com/twisted/twisted@trunk --upgrade
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "runner.py"]
