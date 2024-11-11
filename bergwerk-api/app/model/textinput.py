from pydantic import BaseModel

class TextInput(BaseModel):
    textinput: str
    language: str
    uid: str
