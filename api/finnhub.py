import finnhub
from datetime import datetime, timedelta
import time

finnhub_client = finnhub.Client(api_key="c59shsqad3i93kd215jg")

def fetch_stock_news(symbol):

    news = []
    new_news = None
    start_date = datetime.utcnow().date() - timedelta(days=366)
    end_date = datetime.utcnow().date()

    while new_news != []:

        if new_news is not None:
            time.sleep(1)
        
        new_news = finnhub_client.company_news(symbol, _from=start_date, to=end_date.isoformat())
        news += new_news
        end_date = min(
            end_date - timedelta(days=1),
            datetime.utcfromtimestamp(news[-1]['datetime']).date()
        )
    
    news_df = pd.DataFrame(news).drop_duplicates()

    return news_df