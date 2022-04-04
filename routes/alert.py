from fastapi import APIRouter
from typing import List
from database import database as db
from schemas.news import News
from datetime import datetime, date as dtdate, timedelta

router = APIRouter()

@router.get("", response_model=List[dict])
def get_alerts(counterparty: str = None, date: str = None):
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
        result.append(alert)
    
    return result
    