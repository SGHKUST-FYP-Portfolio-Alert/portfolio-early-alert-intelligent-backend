from fastapi import APIRouter
from database import database as db
from schemas.calculation import Calculation
from typing import List

router = APIRouter()

@router.get("", response_model=List[Calculation])
def get_calculation(counterparty: str):
    filter = {"counterparty": counterparty}
    return list(db.get_calculation(filter))