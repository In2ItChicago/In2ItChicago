FROM python:3.6.6

WORKDIR /clipboardsite
COPY . /clipboardsite

RUN pip3 install -r requirements.txt
RUN chmod +x startup.sh
ENTRYPOINT ["sh", "startup.sh"]
