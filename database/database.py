from typing import List
from pymongo import MongoClient, ReplaceOne
from pymongo.collection import ReturnDocument

client = MongoClient(
    "mongodb+srv://analytics:71mpmU8Lw5ngKhe6@cluster0.lln5s.mongodb.net/"
)

database = client['portfolio_alert']

counterparty_collection = database.get_collection('counterparty')
news_collection = database.get_collection('news')

def add_counterparty(counterparty: dict):
    return counterparty_collection\
        .find_one_and_replace(counterparty, counterparty, upsert=True, return_document=ReturnDocument.AFTER) #upsert operation


def get_counterparties():
    return counterparty_collection.find()


def add_news(news_datum: List[dict]):
    operations = [ 
        ReplaceOne(news_data, news_data, upsert=True) #Upsert operation
        for news_data in news_datum
    ]  

    news_collection.bulk_write(operations)
    return

def get_news(filter, limit=None):
    return news_collection\
        .find(filter, limit=limit)
