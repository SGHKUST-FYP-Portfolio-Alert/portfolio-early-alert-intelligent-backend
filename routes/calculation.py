from collections import defaultdict
from typing import List

from database import database as db
from fastapi import APIRouter
from schemas.calculation import ChartData

router = APIRouter()

'''Returns all data points for a counterparty as a list of dictionaries'''
@router.get("/chart", response_model=List[ChartData])
def get_chart(counterparty: str):
    filter = {"counterparty": counterparty}
    sent_data = list(db.get_sent_calculation(filter))
    sent_data = {x['date']: {'average_score': x['average_score']} for x in sent_data}

    counterparty_status = db.get_one_counterparty_ingest_status({'symbolRef': counterparty})
    stock_data = {}
    if counterparty_status:
        stock_data = list(db.get_counterparty_stock_candles({'counterpartyId': counterparty_status['counterpartyId']}))
        stock_data = {x['date'].strftime('%Y-%m-%d'): {'closing_stock_price': x['Close']} for x in stock_data}

    #merge all dicts/plots
    dd = defaultdict(dict)
    for d in (sent_data, stock_data): # you can list as many input dicts as you want here
        for key, value in d.items():
            name = list(value.keys())[0]
            dd[key][name] = value[name]

    ret = [{'date': key, **item} for key, item in dd.items()] #very messy sorry

    return ret

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
