FROM data_engine

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./data_engine ./data_engine
RUN chmod +x ./clipboard_common_lib/install-common-libs.sh
RUN ["bash", "./clipboard_common_lib/install-common-libs.sh"]

WORKDIR /usr/src/app/data_engine
ENTRYPOINT ["python3", "runner.py"]