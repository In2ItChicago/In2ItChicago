FROM clipboard_db_client

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./clipboard_db_client ./clipboard_db_client
RUN chmod +x ./clipboard_common_lib/install-common-libs.sh
RUN ["bash", "./clipboard_common_lib/install-common-libs.sh"]

WORKDIR /usr/src/app/clipboard_db_client
ENTRYPOINT ["python3", "clipboard_db_client.py"]