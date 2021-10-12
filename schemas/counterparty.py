from pydantic import BaseModel
from typing import Optional

class CounterpartyBase(BaseModel):
    name: str
    symbol: Optional[str]

class CounterpartyCreate(CounterpartyBase):
    pass

class Counterparty(CounterpartyBase):
    pass