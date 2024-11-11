from pydantic import BaseModel

class SectionWikitext(BaseModel):
    host: str
    page: str
    pageid: int
    section: int
    wikitext: str


