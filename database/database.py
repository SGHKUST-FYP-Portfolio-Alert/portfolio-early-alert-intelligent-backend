from typing import List
import motor.motor_asyncio
from pymongo import ReplaceOne

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://analytics:71mpmU8Lw5ngKhe6@cluster0.lln5s.mongodb.net/"
)

database = client['portfolio_alert']

# demo_collection = database.get_collection('demo')
news_collection = database.get_collection('news')

# async def retrieve_demo():
#     demos = []
#     async for demo in demo_collection.find():
#         demos.append(demo)
#     return demos

# async def add_demo(demo_data: dict):
#     await demo_collection.insert_one(demo_data)
#     return

async def add_news(news_data: List[dict]):
    operations = [ 
        ReplaceOne(news_datum, news_datum, upsert=True) 
        for news_datum in news_data 
    ]

    await news_collection.write_bulk(operations)
    return