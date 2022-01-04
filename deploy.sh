#!/bin/bash

echo "-- updating database --"
sh ./data/update-db.sh

# Fail build, if database update fails.
res=`grep ERROR: db.log | awk '{ print $1 }' | tail -1`

if [ "$res" = "ERROR:"  ]; then
   echo "Database error!"
   exit 1;
else
   echo "Database updated."
   # exit 0;
fi

echo "-- Deploy --"
sudo rsync -ar ${APP_SRC}/* ${APP_API}
curl -X Get "http://13.126.95.15:5000/api/buildDetails?storeInDb=1"
