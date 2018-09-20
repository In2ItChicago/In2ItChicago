FROM python:3.7

WORKDIR /clipboarddbclient
COPY . /clipboarddbclient/

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "clipboard_dbclient.py"]
