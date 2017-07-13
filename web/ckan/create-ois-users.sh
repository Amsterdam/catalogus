#!/usr/bin/env bash
# Create users if they are not created

cd /src/ckan

paster user add employee_plus password=insecure \
                              name=employee_plus \
                              fullname=employee_plus \
                              email=not-real@employee_plus.amsterdam.nl -c /app/api.ini

paster user add open password=insecure \
                     name=open \
                     fullname=open \
                     email=not-real@open.amsterdam.nl -c /app/api.ini

paster user add employee password=insecure \
                         name=employee \
                         fullname=employee email=not-real@employee.amsterdam.nl -c /app/api.ini

