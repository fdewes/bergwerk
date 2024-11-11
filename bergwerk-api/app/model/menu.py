from pydantic import BaseModel

class MenuItem(BaseModel):
    title: str
    link: str

class MenuResponse(BaseModel):
    title: str
    text: str
    menuitems: list[MenuItem]


