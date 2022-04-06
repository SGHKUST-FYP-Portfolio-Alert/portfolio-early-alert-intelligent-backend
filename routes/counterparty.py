from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError
from database import database as db
from schemas.counterparty import CounterpartyCreate, Counterparty
from typing import List
from ext_api.finnhub_wrapper import finnhub_client

router = APIRouter()

@router.get("", response_model=List[Counterparty], response_model_exclude_none=True)
def get_counterparties(symbol: str = None, detailed=False):

    filter = {}
    if symbol:
        filter['symbol'] = symbol
    
    result = []
    for counterparty in db.get_counterparties(filter):
        if detailed:
            counterparty['data'] = next(db.get_calculations({'counterparty': counterparty['symbol']}).limit(1), None)
        result.append(counterparty)
    
    return result


@router.post("", response_model=Counterparty, status_code=201)
def add_counterparty(counterparty: CounterpartyCreate):
    counterparty = jsonable_encoder(counterparty)
    try:
        db.add_counterparty(counterparty)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="Counterparty already existed")


@router.delete("")
def delete_counterparty(symbol: str):
    deleted_count = db.delete_counterparty(symbol)
    if deleted_count:
        return
    else:
        raise HTTPException(status_code=404, detail="Counterparty not found")


@router.get("/search")
def search_counterparties(query: str):
    return finnhub_client.symbol_lookup(query)