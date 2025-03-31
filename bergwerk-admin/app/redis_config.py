import redis
import json

r = redis.Redis(host='redis', port=6379, decode_responses=True)

# DEFAULTS = {
#     "error_message": "Oops! Something went wrong. Ups! Hier funktionert etwas nicht!",
#     "initial_greeting": "Um den Chatbot nutzen zu können, müssen Sie bitte unserer Datenschutzerklärung zustimmen. \n\n To proceed, please agree to our chatbot's privacy policy.",
#     "inactivity_timer": "60",
#     "English_llm_models_training_list": "gemma3, gemma3:1b, deepseek-r1:1.5b, deepseek-r1:7b, llama3.2:1b, llama3.2:3b",
#     "Deutsch_llm_models_training_list": "gemma3, gemma3:1b, deepseek-r1:1.5b, deepseek-r1:7b, llama3.2:1b, llama3.2:3b",
#     "English_llm_models_training_instruction": "Read the text below, which could serve as an answer to various questions...",
#     "Deutsch_llm_models_training_instruction": "Lies den folgenden Text, der als Antwort auf verschiedene Fragen dienen könnte. Bitte formuliere fünf bis zehn plausible Fragen..."
# }

DEFAULTS = {
}

def init_defaults():
    for k, v in DEFAULTS.items():
        r.setnx(k, v)

def get_all_config():
    return {k: r.get(k) for k in DEFAULTS.keys()}

def update_config(new_data):
    for k, v in new_data.items():
        r.set(k, v)
