import finnhub
from datetime import datetime, timedelta
import time
import pandas as pd

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
    
    news_df = pd.DataFrame(news).drop_duplicates()

    return news_df

def fetch_1day_stock_news(symbol):

    start_date = datetime.utcnow.date() - timedelta(days=1) #yesterday
    end_date = datetime.utcnow.date()   #today

    news = finnhub_client.company_news(symbol, _from=start_date.isoformat(), to=end_date.isoformat())

    return pd.DataFrame(news)