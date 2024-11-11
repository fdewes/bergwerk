class State:

    def __init__(self):
        self.state = {}

    def add_uid(self, uid):
        self.state[uid] = {}

    def del_uid(self, uid):
        if uid in self.state:
            del self.state[uid]

    def check_uid(self, uid):
        if uid in self.state:
            return True
        else:
            return False

    def set_state(self, uid, k, v):
        if uid in self.state:
            self.state[uid][k] = v
            return True
        else:
            return False

    def get_state(self, uid, k):
        if uid in self.state and k in self.state[uid]:
            return self.state[uid][k]
        else:
            return None
