#!/bin/bash
set -e

# Replace placeholders in SQL file with environment variables
sed -e "s/MYSQL_USER_PLACEHOLDER/${SQL_USER}/g" \
    -e "s/MYSQL_PASS_PLACEHOLDER/${SQL_PASS}/g" \
    /init/init-template.sql > /docker-entrypoint-initdb.d/init.sql

if [ ! -f /etc/mysql/ssl/server-key.pem ]; then
    mkdir -p /etc/mysql/ssl
    openssl genrsa 2048 > /etc/mysql/ssl/server-key.pem
    openssl req -new -x509 -nodes -days 3650 \
        -key /etc/mysql/ssl/server-key.pem \
        -out /etc/mysql/ssl/server-cert.pem \
        -subj "/CN=mysql-server"
    chown -R mysql:mysql /etc/mysql/ssl
    chmod 600 /etc/mysql/ssl/server-key.pem
fi

# Execute the original MySQL entrypoint script
exec /usr/local/bin/docker-entrypoint.sh "$@"
