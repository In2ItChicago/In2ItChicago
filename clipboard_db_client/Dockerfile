FROM clipboarddbclient:latest

WORKDIR /clipboarddbclient
ADD ./clipboard_dbclient.py /clipboarddbclient
ADD ./requirements.txt /clipboarddbclient

RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "clipboard_dbclient.py"]