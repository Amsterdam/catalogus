FROM ubuntu:16.04
MAINTAINER datapunt.ois@amsterdam.nl

ARG CATALOGUS_OBJECTSTORE_PASSWORD
ENV CATALOGUS_OBJECTSTORE_PASSWORD=$CATALOGUS_OBJECTSTORE_PASSWORD

EXPOSE 5000

# Preventing frontend error
RUN export DEBIAN_FRONTEND="noninteractive"
# Apt-ing
RUN apt-get update \
	&& apt-get install -y \
		postgresql \
		libpq-dev \
		git-core \
		redis-server \
		vim \
		sudo \
		python-dev \
		python-pip \
		python-virtualenv \
		netcat-openbsd \
        build-essential build-essential libcurl4-openssl-dev libxml2-dev \
        libssl-dev libfuse-dev libjson-c-dev wget pkg-config fuse \
        curl wget unzip \
	&& apt-get clean \
	&& pip install --upgrade pip \
	## Install cloudfuse
	&& wget https://github.com/redbo/cloudfuse/archive/master.zip \
	&& unzip master.zip && cd cloudfuse-master \
    && ./configure && make && make install && cd ..


# Adding user
RUN adduser --system ckan

# Installing UWSGI en CKAN
RUN pip install -e 'git+https://github.com/ckan/ckan.git@ckan-2.6.0#egg=ckan'
# Installing CKAN dependencies

# Inject setuptools 20.4 to prevent exception
RUN sed -i '1s/^/setuptools==20.4 /' /src/ckan/requirements.txt
RUN echo "datapunt-authorization==0.2.0" >> /src/ckan/requirements.txt
RUN echo "PyJWT>=1.4.2" >> /src/ckan/requirements.txt


RUN pip install -r /src/ckan/requirements.txt
RUN mkdir -p /etc/ckan/default \
	&& mkdir /home/ckan/etc \
	&& mkdir /var/lib/ckan \
	&& chown -R ckan /etc/ckan /var/lib/ckan

# Copy plugins
COPY ckanext-dcatAmsterdam /src/ckanext-dcatAmsterdam
COPY ckanext-iauthfunctions /src/ckanext-iauthfunctions

WORKDIR /src/ckanext-dcatAmsterdam
# make sure the the plugins are installed in develop mode
RUN python setup.py develop

WORKDIR /src/ckanext-iauthfunctions
RUN python setup.py develop

RUN chown -R ckan /src/ckanext-*

# Setting ckan app
USER ckan
COPY ckan /app/


RUN export CKAN_INI=/app/config.ini

CMD /app/docker-entrypoint.sh
