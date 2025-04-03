FROM python:3.11

WORKDIR /app


RUN pip install fastapi uvicorn jinja2 aiofiles python-multipart redis requests

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
