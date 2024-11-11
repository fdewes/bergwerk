# Bergwerk Cron

This file builds the container for the **Bergwerk Cron Service**. The cron service  regularly logs conversations stored in the Bergwerk MySQL database into the Bergwerk wiki. This log enables easy review of user interactions, allowing administrators to improve and expand chatbot content based on actual user input.

### Default Schedule

The conversation logging job runs at a default interval of **once every hour**, which can be adjusted in the `crontab` file to fit specific needs. By default, the job runs at the first minute of every hour:

```
1 * * * * bash -c "/usr/local/bin/python /usr/src/app/tracker.py >> /var/log/cron.log 2>&1"
```

This cron job setup initiates the `tracker.py` script, which writes the conversation logs to the wiki.

This automated tracking process helps keep the chatbot’s knowledge base updated and ensures continuous improvement based on user interactions.
### Crontab Time Format

The crontab time format consists of five fields that define the timing of the job:

```
* * * * *
| | | | |
| | | | └─── Day of the week (0 - 7) (Sunday is 0 or 7)
| | | └───── Month (1 - 12)
| | └─────── Day of the month (1 - 31)
| └───────── Hour (0 - 23)
└─────────── Minute (0 - 59)
```

In the example above, `1 * * * *` means the job runs at the **first minute of every hour**.


## docker-compose.yaml

```Dockerfile
--8<-- "bergwerk-cron/Dockerfile"
```