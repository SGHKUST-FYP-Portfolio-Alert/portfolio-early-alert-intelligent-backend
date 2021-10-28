import logging
import time
from datetime import datetime, timedelta

import finnhub
import pandas as pd

logger = logging.getLogger(__name__)

finnhub_client = finnhub.Client(api_key="c59shsqad3i93kd215jg")

def fetch_historical_stock_news(symbol):

    news = []
    new_news = None
    start_date = datetime.utcnow().date() - timedelta(days=366) #finnhub free tier provide one year historical news
    end_date = datetime.utcnow().date() #today

    while new_news != []:

        if new_news is not None:
            time.sleep(1)
        
        new_news = finnhub_client.company_news(symbol, _from=start_date.isoformat(), to=end_date.isoformat())
        news += new_news
        end_date = min(
            end_date - timedelta(days=1),
            datetime.utcfromtimestamp(news[-1]['datetime']).date()
        )
    
    news_df = pd.DataFrame(news).drop_duplicates(subset=['datetime', 'headline', 'source'])
    news_df['api'] = 'Finnhub'
    news_df['counterparty'] = symbol

    news_df\
        .drop(columns=['category', 'id', 'related'], inplace=True)

    return news_df.to_dict('records')

def fetch_1day_stock_news(symbol):

    start_date = datetime.utcnow().date() - timedelta(days=1) #yesterday
    end_date = datetime.utcnow().date()   #today

    news = finnhub_client.company_news(symbol, _from=start_date.isoformat(), to=end_date.isoformat())

    news_df = pd.DataFrame(news).drop_duplicates(subset=['datetime', 'headline', 'source'])
    news_df['api'] = 'Finnhub'

    news_df['counterparty'] = symbol

    news_df\
        .drop(columns=['category', 'id', 'related'], inplace=True)

    return news_df.to_dict('records')

# finnhub free tier provide one year historical 
# def fetch_historical_daily_stock_candles(symbol: str, start: int = 366, end: int = 0):
#     if start <= end:
#         logger.warning('Input params warning, empty return')
#         return {}

#     start_date = datetime.utcnow().date() - timedelta(days=start)
#     end_date = datetime.utcnow().date() - timedelta(days=end)

#     test = finnhub_client.stock_candles(symbol, 'D', 
#         int(time.mktime(start_date.timetuple())), int(time.mktime(end_date.timetuple())))

#     print('sym', symbol, 'len', len(test['c']))

#     #not all 365 days are fetched, since some days are holidays but no way to know how yet

#     # breakpoint()
