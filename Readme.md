### Eenmalige setup DB

    Import the latest database from acceptance:

    $ docker-compose exec database update-db.sh catalogus


### Aanmaken sysadmin account

    $ paster sysadmin add <user-name> -c /app/config.ini

Je wordt daarna gevraagd een password aan te maken als deze gebruiker nog niet bestaat





To import the latest database from acceptance:

    docker-compose exec database update-db.sh catalogu
