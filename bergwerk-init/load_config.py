import yaml
import redis
import json

def load_config(yaml_path="config.yaml", redis_host="redis"):
    # Read YAML
    with open(yaml_path, 'r') as file:
        raw_config = yaml.safe_load(file)

    # Serialize any lists/dicts as JSON strings
    config = {}
    for key, value in raw_config.items():
        if isinstance(value, (list, dict)):
            config[key] = json.dumps(value)
        else:
            config[key] = str(value)

    r = redis.Redis(host=redis_host, port=6379, db=0)

    r.hset("config:app", mapping=config)
    print(f"Loaded config into Redis: {config}")

if __name__ == "__main__":
    load_config()
