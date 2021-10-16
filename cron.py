from api import finnhub
from database import database as db

def daily_update_cron():

    print("daily update in progress")

    for counterparty in db.get_counterparties():
        if not db.news_collection.find_one({'counterparty': counterparty['symbol'] or counterparty['name']}):
            news = finnhub.fetch_historical_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)
    
        else:
            news = finnhub.fetch_1day_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)
    
    print("daily update completed")




