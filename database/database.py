from typing import List
import motor.motor_asyncio
from pymongo import ReplaceOne

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://analytics:71mpmU8Lw5ngKhe6@cluster0.lln5s.mongodb.net/"
)

database = client['portfolio_alert']

counterparty_collection = database.get_collection('counterparty')
news_collection = database.get_collection('news')

async def add_counterparty(counterparty: dict):
    await counterparty_collection\
        .replace_one(counterparty, counterparty, upsert=True) #upsert operation
    
    return

async def get_counterparties():
    return await counterparty_collection.find().to_list(None)


async def add_news(news_datum: List[dict]):
    operations = [ 
        ReplaceOne(news_data, news_data, upsert=True) #Upsert operation
        for news_data in news_datum
    ]  

    await news_collection.bulk_write(operations)
    return

async def get_news(filter, limit=None):
    return await news_collection\
        .find(filter)\
        .to_list(limit)

