from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from database import database as db
from schemas.counterparty import CounterpartyCreate, Counterparty
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Counterparty])
def get_counterparties():
    return list(db.get_counterparties())


@router.post("/", response_model=Counterparty)
def add_counterparty(counterparty: CounterpartyCreate):
    counterparty = jsonable_encoder(counterparty)
    return db.add_counterparty(counterparty)

