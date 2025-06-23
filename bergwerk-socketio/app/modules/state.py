import redis
import json

class State:

    def __init__(self):
        self.redis_client = redis.Redis(host='redis', port=6379, db=0)

    def add_uid(self, uid):
        self.redis_client.hset(uid, "initialized", 1)

    def del_uid(self, uid):
        self.redis_client.delete(uid)

    def check_uid(self, uid):
        return self.redis_client.exists(uid) == 1

    def set_state(self, uid, k, v):
        if self.check_uid(uid):
            v = json.dumps(v)
            self.redis_client.hset(uid, k, v)
            return True
        else:
            return False

    def get_state(self, uid, k):
        if self.check_uid(uid):
            value = self.redis_client.hget(uid, k)
            if value:
                return json.loads(value)
        return None