import requests
import json


def load_model(model):
    url = "http://ollama:11434/api/pull"
    payload = {
        "model": model,
    }

    response = requests.post(url, json=payload)
    return response

def delete_model(model):
    url = "http://ollama:11434/api/delete"
    payload = {
        "model": model,
    }

    response = requests.post(url, json=payload)
    return response

def query_llm(textinput, model):

    url = "http://ollama:11434/api/generate"
    payload = {
        "model": model,
        "stream": False,
        "prompt": textinput
    }

    response = requests.post(url, json=payload)
    to = json.loads(response.text)

    return to['response']
