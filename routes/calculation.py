from collections import defaultdict
from typing import List

from database import database as db
from fastapi import APIRouter
from schemas.calculation import ChartData

router = APIRouter()

'''Returns all data points for a counterparty as a list of dictionaries'''
@router.get("/chart", response_model=List[ChartData], response_model_exclude_none=True)
def get_chart(counterparty: str):
    filter = {"counterparty": counterparty}
    sent_data = list(db.get_sent_calculation(filter))

    return sent_data

    #merge all dicts/plots
    # resp = []
    # all_keys = set(list(sent_data.keys()) + list(stock_data.keys()))
    
    # for key in all_keys:
    #     null_val = -1
    #     resp.append({
    #         'date': key,
    #         'average_score': sent_data[key] if key in sent_data else null_val,
    #         'closing_stock_price': stock_data[key] if key in stock_data else null_val,
    #         })
