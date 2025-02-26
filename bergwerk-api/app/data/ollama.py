import requests
import json

def query_llm(textinput):

    url = "http://ollama:11434/api/generate"
    payload = {
        "model": "llama3.2:1b",
        "stream": False,
        "prompt": textinput
    }

    response = requests.post(url, json=payload)
    to = json.loads(response.text)

    return to