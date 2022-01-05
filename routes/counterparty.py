from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError
from database import database as db
from schemas.counterparty import CounterpartyCreate, Counterparty
from typing import List
from ext_api.finnhub_wrapper import finnhub_client

router = APIRouter()

@router.get("", response_model=List[Counterparty])
def get_counterparties():
    return list(db.get_counterparties())


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