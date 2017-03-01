### Eenmalige setup DB

    Import the latest database from acceptance:

    $ docker-compose exec database update-db.sh catalogus


### Aanmaken sysadmin account

    $ paster sysadmin add <user-name> -c /app/config.ini

Je wordt daarna gevraagd een password aan te maken als deze gebruiker nog niet bestaat


### Importeer de laatst database van acceptance:

    docker-compose exec database update-db.sh catalogus
    
### Toevoegen van de 3 ois gebruikers `open`, `employee` en `employee_plus`

    $ docker-compose exec ckan /app/create_ois_users.sh -c /app/config.ini
