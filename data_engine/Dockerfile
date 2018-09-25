FROM python:3.7

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./data_engine ./data_engine
COPY ./install-common-libs.sh ./install-common-libs.sh
RUN chmod +x ./install-common-libs.sh
RUN ["bash", "./install-common-libs.sh"]

WORKDIR /usr/src/app/data_engine
# Move this back into requirements.txt when new twisted version is released
RUN pip3 install git+https://github.com/twisted/twisted@992a841506d18a77f8fa15efe4b957e02075a1a1 --upgrade
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "runner.py"]