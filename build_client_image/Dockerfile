FROM python:latest

RUN wget http://packages.couchbase.com/releases/couchbase-release/couchbase-release-1.0-4-amd64.deb \
	&& apt-get update \
	&& apt-get install -y lsb-release \
	&& dpkg -i couchbase-release-1.0-4-amd64.deb \
	&& apt-get update \
	&& apt-get install -y libcouchbase-dev build-essential python3-dev
RUN ["rm", "couchbase-release-1.0-4-amd64.deb"]