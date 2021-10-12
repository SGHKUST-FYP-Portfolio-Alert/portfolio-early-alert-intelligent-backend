from api import finnhub
from database import database as db

async def daily_update_cron():

    for counterparty in await db.get_counterparties():
        if not db.get_news({'counterparty_id': counterparty['_id']}, 1):
            news = finnhub.fetch_historical_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)
    
        else:
            news = finnhub.fetch_1day_stock_news(counterparty['symbol'] or counterparty['name'])
            db.add_news(news)




