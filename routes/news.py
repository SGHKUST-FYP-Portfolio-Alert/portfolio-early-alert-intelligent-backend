from fastapi import APIRouter
from typing import List
from fastapi.encoders import jsonable_encoder
from database import database as db
from schemas.news import News

router = APIRouter()

@router.get("/", response_model=List[News])
def get_news(counterparty: str = None, skip: int = 0, limit: int = 0):
    if counterparty is not None:
        news_filter = {'counterparty': counterparty}
    else:
        news_filter = {}
    return list(db.get_news(news_filter, skip=skip, limit=limit))
    