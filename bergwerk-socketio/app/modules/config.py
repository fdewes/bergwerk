import requests
from icecream import ic

class Config:

    def __init__(self):
        self.config = {}

    def get_value(self, k):
        if self.config == {}:
            response = requests.get("http://bergwerk-api/wiki/config")
            data = response.json()  # Assuming the response is in JSON format
            self.config = {x['key']:x['value'] for x in data}

        return self.config[k].replace("\\n\\n", "\n\n")
