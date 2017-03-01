#!/usr/bin/env bash

set -u
set -e

# wait for postgres to be started
while ! netcat -z ${DATABASE_PORT_5432_TCP_ADDR} ${DATABASE_PORT_5432_TCP_PORT}
do
	echo "Waiting for solr..."
	sleep 1
done

# wait for solr to be started
while ! netcat -z ${SOLR_PORT_8983_TCP_ADDR} ${SOLR_PORT_8983_TCP_PORT}
do
	echo "Waiting for solr..."
	sleep 1
done

echo Building db

cd /src/ckan
cloudfuse -o username=catalogus,password=${CATALOGUS_OBJECTSTORE_PASSWORD},tenant=e85bcf2124fb4437b1bc6eb75dfc3abf,authurl=https://identity.stack.cloudvps.com/v2.0 /var/lib/ckan/

# init database
paster db init -c /app/config.ini
# rebuild solr index
paster search-index rebuild -c /app/config.ini

# start service
paster serve /app/config.ini
