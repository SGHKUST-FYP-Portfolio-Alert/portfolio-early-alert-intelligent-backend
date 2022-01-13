from database import database as db
from datetime import timezone
import datetime

def aggregate_sentiments_daily():
    
    pipeline = [
        {'$group': {'_id': { 'date': '$date', 'counterparty': '$counterparty', 'sentiment': '$sentiment'}, 'count':{'$sum':1}}},
        {'$group': {'_id': {'date':'$_id.date', 'counterparty':'$_id.counterparty'}, 'sentiments': {'$addToSet' : {'k': {'$toString': '$_id.sentiment'}, 'v':'$count'}}}},
        {'$project': {'_id': 0, 'date':'$_id.date', 'counterparty':'$_id.counterparty', 'sentiments': {'$arrayToObject': '$sentiments'} }}
    ]

    return db.aggregate_news(pipeline)


def aggregate_keywords_daily():

    pipeline =  [
        {'$group': {'_id': {'date': '$date', 'counterparty':'$counterparty'}, 'keyword_count': {'$mergeObjects': '$keyword_count'}}},
        {'$project': {'_id': 0, 'date':'$_id.date', 'counterparty':'$_id.counterparty', 'keyword_count': '$keyword_count'}}
    ]

    return db.aggregate_news(pipeline)
