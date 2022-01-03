import datetime
import logging
from typing import List

from pymongo import ASCENDING, DESCENDING, MongoClient, ReplaceOne, UpdateOne
from pymongo.collection import ReturnDocument

client = MongoClient(
    "mongodb+srv://analytics:71mpmU8Lw5ngKhe6@cluster0.lln5s.mongodb.net/"
)

logger = logging.getLogger(__name__)
database = client['portfolio_alert']

counterparty_collection = database.get_collection('counterparty')
counterparty_ingest_status_collection = database.get_collection('counterparty_ingest_status')
counterparty_daily_stock_collection = database.get_collection('counterparty_daily_stock_price')
news_collection = database.get_collection('news')
calculation_collection = database.get_collection('calculation')

def add_counterparty(counterparty: dict):
    return counterparty_collection\
        .find_one_and_replace(counterparty, counterparty, upsert=True, return_document=ReturnDocument.AFTER) #upsert operation

def get_counterparties():
    return counterparty_collection.find()


def get_one_counterparty_ingest_status(query):
    return counterparty_ingest_status_collection.find_one(query)

def update_counterparty_ingest_status(query, update):
    return counterparty_ingest_status_collection.find_one_and_replace(query, update, upsert=True, return_document=ReturnDocument.AFTER)


def add_counterparty_stock_candles(candles):
    for candle in candles:
        if 'date' not in candle:
            logger.error('Candle must have date')
            return False
        else:
            temp = candle['date']
            candle['date'] = datetime.datetime(temp.year, temp.month, temp.day)

    try:
        result = counterparty_daily_stock_collection.insert_many(candles)
    except Exception as e:
        logger.warning('Could not insert. Exception: '+str(e))
        return False

    if len(result.inserted_ids) != len(candles):
        logger.error('Not all candles inserted')

    return result

def get_counterparty_stock_candles(filter):
    return counterparty_daily_stock_collection.find(filter)

def add_news(news_datum: List[dict]):
    if not news_datum:
        return  # skip operations if news_datum is empty

    operations = [ 
        ReplaceOne(news_data, news_data, upsert=True) #Upsert operation
        for news_data in news_datum
    ]  

    news_collection.bulk_write(operations)
    return

def update_news(news_datum: List[dict]):
    # [{"_id": XXX, "sentiment": "positive"}, {"_id": XXX, "sentiment": "negative"}]

    if not news_datum:
        return  # skip operations if news_datum is empty

    operations = [
        UpdateOne(
            {"_id": news_data["_id"] },
            {"$set": news_data}
        )
        for news_data in news_datum
    ]

    news_collection.bulk_write(operations)
    return

def get_news(filter, skip: int = 0, limit: int = 0, sort = False):
    if sort:
        return news_collection\
            .find(filter)\
            .sort('datetime', DESCENDING)\
            .skip(skip)\
            .limit(limit)
    else:
        return news_collection\
            .find(filter)\
            .skip(skip)\
            .limit(limit)

def aggregate_news(pipeline):
    return news_collection\
        .aggregate(pipeline)


def add_calculation(calculation_datum: List[dict]):
    if not calculation_datum:
        return

    operations = [ 
        ReplaceOne(calculation_data, calculation_data, upsert=True) #Upsert operation
        for calculation_data in calculation_datum
    ]  

    calculation_collection.bulk_write(operations)
    return

def update_calcution(calculation_datum: List[dict]):
    # [{"_id": XXX, "counterparty": "positive"}, {"_id": XXX, "counterparty": "negative"}]
    if not calculation_datum:
        return

    operations = [
        UpdateOne(
            {"_id": calculation_data["_id"] },
            {"$set": calculation_data}
        )
        for calculation_data in calculation_datum
    ]
    calculation_collection.bulk_write(operations)
    return

def get_sent_calculation(filter):
    return calculation_collection\
        .find(filter)\
        .sort('date', ASCENDING)
