FROM python:3.7

# Move this back into requirements.txt when new twisted version is released
RUN pip3 install git+https://github.com/twisted/twisted@992a841506d18a77f8fa15efe4b957e02075a1a1 --upgrade
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
