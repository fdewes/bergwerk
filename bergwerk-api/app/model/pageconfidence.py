from pydantic import BaseModel

class PageConfidence(BaseModel):
    title: str
    confidence: float