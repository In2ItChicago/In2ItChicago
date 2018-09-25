FROM python:3.7

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./clipboard_db_client ./clipboard_db_client
COPY ./install-common-libs.sh ./install-common-libs.sh
RUN chmod +x ./install-common-libs.sh
RUN ["bash", "./install-common-libs.sh"]

WORKDIR /usr/src/app/clipboard_db_client
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "clipboard_dbclient.py"]