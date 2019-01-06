FROM python:3.7.1 AS data_engine_deps
RUN pip3 install -U pip
# Move this back into requirements.txt when new twisted version is released
#RUN pip3 install git+https://github.com/twisted/twisted@992a841506d18a77f8fa15efe4b957e02075a1a1 --upgrade
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

FROM data_engine_deps
WORKDIR /usr/src/app
COPY . ./data_engine
WORKDIR /usr/src/app/data_engine
ENTRYPOINT ["python3", "runner.py"]
