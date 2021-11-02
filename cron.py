from ext_api import finnhub_wrapper
from database import database as db
from models.modelInfer import modelInfer
import models.config as modelConfig
from datetime import timezone
import datetime
from tqdm import tqdm

def daily_update_cron():
    print("daily update in progress")
        
    add_news() 
    add_sentiment()
    add_date()
    print("daily update completed")

def add_news():
    print("Start adding news")
    for counterparty in db.get_counterparties():
        if not db.news_collection.find_one({'counterparty': counterparty['symbol'] or counterparty['name']}):
            news = finnhub_wrapper.fetch_historical_stock_news(counterparty['symbol'] or counterparty['name'])
        else:
            news = finnhub_wrapper.fetch_1day_stock_news(counterparty['symbol'] or counterparty['name'])
        db.add_news(news)

    
def add_sentiment():
    # start_dt = datetime.datetime(2021, 10, 14)
    # unix_start_dt = start_dt.replace(tzinfo=timezone.utc).timestamp()
    # end_dt = datetime.datetime(2021, 10, 16)
    # unix_end_dt = end_dt.replace(tzinfo=timezone.utc).timestamp()
    print("Start adding sentiment")
    filter = {"sentiment":{"$exists": False}}
    news_no_sentiment = list(db.get_news(filter))
    myModel = modelInfer(news_no_sentiment,modelConfig)
    infered_result = myModel.infer()
    db.update_news(infered_result)

def add_date():
    filter = {"date":{"$exists": False}}
    news_no_date = list(db.get_news(filter))
    result_list = []
    id_loop = [data['_id'] for data in news_no_date]
    print(type(news_no_date), type(id_loop))
    print("Start adding dates")
    for id, news in tqdm(zip(id_loop,news_no_date),total=len(id_loop)):
        value = datetime.datetime.fromtimestamp(news["datetime"])
        date = f"{value:%Y-%m-%d}"
        result_list.append({"_id":id, "date":date})
    db.update_news(result_list)


