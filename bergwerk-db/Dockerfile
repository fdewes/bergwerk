FROM mysql:latest

ENV MYSQL_RANDOM_ROOT_PASSWORD=Yes

COPY custom_init.sh /init/
COPY init-template.sql /init/

RUN chmod +x /init/custom_init.sh

ENTRYPOINT ["/init/custom_init.sh"]

CMD ["mysqld"]