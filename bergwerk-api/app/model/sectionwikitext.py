from pydantic import BaseModel

class SectionWikitext(BaseModel):
    page: str
    pageid: int
    section: int
    wikitext: str


