FROM python:3.7

WORKDIR /usr/src/app
COPY ./clipboard_common_lib ./clipboard_common_lib
COPY ./clipboard_site ./clipboard_site
RUN chmod +x ./clipboard_common_lib/install-common-libs.sh
RUN ["bash", "./clipboard_common_lib/install-common-libs.sh"]

WORKDIR /usr/src/app/clipboard_site
RUN pip3 install -r requirements.txt
RUN chmod +x startup.sh
ENTRYPOINT ["sh", "startup.sh"]
