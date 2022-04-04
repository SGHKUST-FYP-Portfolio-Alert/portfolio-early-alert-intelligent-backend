from xmlrpc.client import boolean
from fastapi import APIRouter
from typing import List
from database import database as db
from schemas.alert import Alert
from datetime import datetime, date as dtdate, timedelta

router = APIRouter()

@router.get("", response_model=List[Alert])
def get_alerts(counterparty: str = None, date: str = None, detailed: bool = False):
    alert_filter = {}
    
    if counterparty is not None:
        alert_filter['counterparty'] =  counterparty
    
        if date is None:
            date = dtdate.today().isoformat()
        alert_filter['date'] = {
            '$lte': datetime.fromisoformat(date),
            '$gte': datetime.fromisoformat(date) - timedelta(days=5)
        }

    result = []

    for alert in db.get_alerts(alert_filter):
        alert['id'] = str(alert['_id'])
        del alert['_id']
        if detailed:
            alert['counterparty'] = db.get_counterparty({'symbol': alert['counterparty']})
        result.append(alert)
    
    return result
    