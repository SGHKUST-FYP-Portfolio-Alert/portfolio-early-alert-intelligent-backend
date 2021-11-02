from pydantic import BaseModel
from typing import Optional

class News(BaseModel):
    counterparty: str
    datetime: int
    headline: str
    image: Optional[str]
    source: str
    summary: Optional[str]
    url: Optional[str]
    api: Optional[str]
    sentiment: Optional[int]
    date: Optional[str]



