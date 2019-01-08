FROM python:3.7.2 AS event_processor_deps
RUN pip3 install -U pip
# Move this back into requirements.txt when new twisted version is released
#RUN pip3 install git+https://github.com/twisted/twisted@992a841506d18a77f8fa15efe4b957e02075a1a1 --upgrade
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

FROM event_processor_deps
WORKDIR /usr/src/app
COPY . ./event_processor
WORKDIR /usr/src/app/event_processor
ENTRYPOINT ["python3", "runner.py"]
