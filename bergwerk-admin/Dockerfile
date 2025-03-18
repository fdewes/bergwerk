# Use official Python image
FROM python:3.11

ENV MEDIAWIKI_ADMIN ${MEDIAWIKI_ADMIN}
ENV MEDIAWIKI_ADMIN_PASSWORD ${MEDIAWIKI_ADMIN_PASSWORD}

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

# Start the application
CMD ["python", "app.py"]
