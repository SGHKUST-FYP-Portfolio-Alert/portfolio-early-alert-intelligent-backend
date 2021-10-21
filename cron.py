from api import finnhub
from database import database as db
from models.modelInfer import modelInfer
import models.config as modelConfig
from datetime import timezone
import datetime

def daily_update_cron():
    print("daily update in progress")
    for counterparty in db.get_counterparties():
        if not db.news_collection.find_one({'counterparty': counterparty['symbol'] or counterparty['name']}):
            news = finnhub.fetch_historical_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)
        else:
            news = finnhub.fetch_1day_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)
    update_sentiment()
    print("daily update completed")
    
def update_sentiment():
    start_dt = datetime.datetime(2021, 10, 14)
    unix_start_dt = start_dt.replace(tzinfo=timezone.utc).timestamp()
    end_dt = datetime.datetime(2021, 10, 16)
    unix_end_dt = end_dt.replace(tzinfo=timezone.utc).timestamp()
    filter = {"sentiment":{"$exists": False}}
    news_no_sentiment = list(db.get_news(filter))
    myModel = modelInfer(news_no_sentiment,modelConfig)
    infered_result = myModel.infer()
    db.update_news(infered_result)



