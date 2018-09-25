FROM python:3.7

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./clipboard_site ./clipboard_site
COPY ./install-common-libs.sh ./install-common-libs.sh
RUN chmod +x ./install-common-libs.sh
RUN ["bash", "./install-common-libs.sh"]

WORKDIR /usr/src/app/clipboard_site
RUN pip3 install -r requirements.txt
RUN chmod +x startup.sh
ENTRYPOINT ["sh", "startup.sh"]
