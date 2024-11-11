class MissingPage(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class MissingSection(Exception):
    def __init__(self, msg: str):
        self.msg = msg
        
class MissingLanguage(Exception):
    def __init__(self, msg: str):
        self.msg = msg

class MissingClassifier(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class Unauthorized(Exception):
    def __init__(self, msg: str):
        self.msg = msg