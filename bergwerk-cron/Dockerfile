FROM python:3.12

ENV BOT_USERNAME ${BOT_USERNAME}
ENV MEDIAWIKI_ADMIN_PASSWORD ${MEDIAWIKI_ADMIN_PASSWORD}

RUN apt-get update && apt-get install -y cron
WORKDIR /usr/src/app
COPY scripts/tracker.py .
COPY scripts/check_content.py .
COPY scripts/env.sh .
COPY requirements.txt .

RUN chmod 755 env.sh


RUN pip install -r requirements.txt

COPY crontab /etc/cron.d/my-cron-job
RUN chmod 0644 /etc/cron.d/my-cron-job
RUN crontab /etc/cron.d/my-cron-job
RUN touch /var/log/cron.log

ENTRYPOINT [ "/usr/src/app/env.sh" ]
