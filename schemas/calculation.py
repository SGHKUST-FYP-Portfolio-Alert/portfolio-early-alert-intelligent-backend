from pydantic import BaseModel
from typing import Optional

class ChartData(BaseModel):
    date: str #format: 2021-12-06
    average_score: Optional[float]
    closing_stock_price: Optional[float]
    keyword_count: Optional[dict]
    news_count: Optional[int]
    sentiments: Optional[dict]