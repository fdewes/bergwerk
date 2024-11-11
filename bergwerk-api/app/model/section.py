from pydantic import BaseModel

class Section(BaseModel):
    page: str
    pageid: int
    line: str
    index: int
    number: str
    toclevel: int