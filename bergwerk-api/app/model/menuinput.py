from pydantic import BaseModel

class MenuInput(BaseModel):
    menuinput: str
    language: str
    uid: str
