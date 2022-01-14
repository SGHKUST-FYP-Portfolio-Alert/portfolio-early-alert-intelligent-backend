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


def aggregate_keywords_news_count_daily():

    pipeline =  [
        {'$group': {'_id': {'date': '$date', 'counterparty':'$counterparty'}, 'keyword_count': {'$mergeObjects': '$keyword_count'}, 'news_count': {'$sum':1}}},
        {'$project': {'_id': 0, 'date':'$_id.date', 'counterparty':'$_id.counterparty', 'keyword_count': 1, 'news_count': 1}}
    ]

    return db.aggregate_news(pipeline)
