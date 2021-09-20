from fastapi import APIRouter
from database import database as db

router = APIRouter()

@router.get("/")
async def get_demo():
    return await db.retrieve_demo()


@router.post("/")
async def post_demo(demo_data: dict):
    await db.add_demo(demo_data)
