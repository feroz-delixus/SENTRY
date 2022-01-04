#!/bin/bash

echo -- update, alter database --
psql -h $DB_HOSTNAME -p $DB_PORT -U $DB_USERNAME -w -d $DATABASE < ./data/pg/update-alter-db.sql > db.log 2>&1
