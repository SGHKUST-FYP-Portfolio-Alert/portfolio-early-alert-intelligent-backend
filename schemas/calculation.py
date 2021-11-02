from pydantic import BaseModel
from typing import Optional

class Calculation(BaseModel):
    date: str
    average_score: float