#!/bin/sh

sleep 5

mediawiki-init.sh 
service php8.3-fpm start 
service nginx start 
python3 /usr/local/bin/load_data.py

echo "Starting…"
exec "$@"