FROM python:3.12

COPY ./app /app
WORKDIR /app

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./data/intent_classifier /intent_classifier

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload", "--root-path", "/api"]
