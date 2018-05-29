FROM python:latest

WORKDIR /clipboarddbclient
ADD ./clipboard_dbclient.py /clipboarddbclient
ADD ./db_locks.py /clipboarddbclient
ADD ./requirements.txt /clipboarddbclient

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "clipboard_dbclient.py"]