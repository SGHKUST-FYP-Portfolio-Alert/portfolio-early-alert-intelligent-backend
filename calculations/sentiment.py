from database import database as db
from datetime import timezone
import datetime

def average():
    news_with_sentiment = list(db.get_news({"sentiment":{"$exists": True}}))
    sum = 0
    aggregated_news = db.aggregate_news([{"$group" : 
                      {"_id" : {"counterparty":"$counterparty","date":"$date"}, 
                      "average_score" : {"$avg" : "$sentiment"}}}])
    new_list = []
    for calculation in aggregated_news:
        empty_dict = {}
        empty_dict['counterparty'] = calculation['_id']['counterparty']
        empty_dict['date'] = calculation['_id']['date']
        empty_dict['average_score'] = calculation['average_score']
        new_list.append(empty_dict)
    db.add_calculation(new_list)
