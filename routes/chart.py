from collections import defaultdict
from typing import List

from database import database as db
from fastapi import APIRouter
from schemas.chart import CalculationData, PriceData

router = APIRouter()

'''Returns all data points for a counterparty as a list of dictionaries'''
@router.get("/calculation", response_model=List[CalculationData], response_model_exclude_none=True)
def get_calculations(counterparty: str):
    filter = {"counterparty": counterparty}
    return list(db.get_calculations(filter))


@router.get("/price", response_model=List[PriceData])
def get_prices(counterparty: str):
    counterparty_status = db.get_one_counterparty_ingest_status({'symbolRef': counterparty})
    if counterparty_status:
        stock_data =  list(db.get_counterparty_stock_candles({'counterpartyId': counterparty_status['counterpartyId']}))
        stock_data = [{**x, 'date': x['date'].strftime('%Y-%m-%d')} for x in stock_data]
        return stock_data
