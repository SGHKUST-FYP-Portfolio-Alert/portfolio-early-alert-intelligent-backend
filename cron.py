import logging
from datetime import datetime, timedelta, timezone

from pymongo.collection import ReturnDocument
from tqdm import tqdm

import models.config as modelConfig
from database import database as db
from ext_api import finnhub_wrapper, yahoo_finance
from models.modelInfer import modelInfer

logger = logging.getLogger(__name__)

def daily_update_cron():
    logger.info("daily update in progress")
    
    check_counterparty_status()

    add_news_datestring()
    add_sentiment()

    logger.info("daily update completed")

def ingest_stock_price(ingest_date, args):
    logger.debug("Start ingesting stock price for "+args['symbol'])

    if ingest_date == None:
        ingest_date = datetime(2000, 1, 1)

    ingest_date += timedelta(days=1)
    hist = yahoo_finance.fetch_historical_daily_stock_candles(args['symbol'], start=ingest_date, end=datetime.now(timezone.utc))
    if not len(hist.index):
        logger.warning(f"No stock price found for {args['symbol']} since {ingest_date}")
        return False
    
    candles = []
    for date, day_range in hist.iterrows():
        doc = {}
        doc['date'] = date
        doc['counterpartyId'] = args['_id']
        doc.update(dict(day_range))
        
        doc['refOnly'] = {'name': args['name'], 'symbol': args['symbol']}

        candles.append(doc)
    
    result = db.add_counterparty_stock_candles(candles)

    if result == False:
        return False
    return True
            

def ingest_news(date, args):
    logger.debug("Ingest news")
    counterparty = args['symbol'] or args['name']
    logger.debug("Start ingesting news for "+counterparty)

    if not date:
        news = finnhub_wrapper.fetch_historical_stock_news(counterparty)
    else:
        news = finnhub_wrapper.fetch_1day_stock_news(counterparty)
    
    try:
        db.add_news(news)
    except Exception as e:
        logger.error("New ingest failed for "+counterparty)
        return False

    return True

def check_counterparty_status():
    logger.debug("Start ingest")

    ingest_functions = [
        ingest_news,
        ingest_stock_price,
    ]

    for counterparty in db.get_counterparties():
        query = {'counterpartyId': counterparty['_id']}
        status = db.get_one_counterparty_ingest_status(query)

        if status == None:
            status = dict(zip([f.__name__ for f in ingest_functions], [None]*len(ingest_functions)))
            status['counterpartyId'] = counterparty['_id']
            status['symbolRef'] = counterparty['symbol']

        args = {**counterparty}

        for func in ingest_functions:
            #run function, save date if successful
            if func(status[func.__name__], args):
                status[func.__name__] = datetime.now(timezone.utc)

        updated = db.update_counterparty_ingest_status(query, status)
        logging.debug('counterparty status updated'+str(updated))

'''
Adds date field with %Y-%m-%d format to each news article collection.
'''
def add_news_datestring():
    filter = {"date":{"$exists": False}}
    news_no_date = db.get_news(filter)
    result_list = []
    for news in news_no_date:
        value = datetime.fromtimestamp(news["datetime"])
        date = f"{value:%Y-%m-%d}"
        result_list.append({"_id": news['_id'], "date":date})
    db.update_news(result_list)

'''
Adds sentiment to news articles without one.
'''
def add_sentiment():
    # start_dt = datetime(2021, 10, 14)
    # unix_start_dt = start_dt.replace(tzinfo=timezone.utc).timestamp()
    # end_dt = datetime(2021, 10, 16)
    # unix_end_dt = end_dt.replace(tzinfo=timezone.utc).timestamp()
    logger.info("Start adding sentiment")
    filter = {"sentiment":{"$exists": False}}
    news_no_sentiment = list(db.get_news(filter))
    myModel = modelInfer(news_no_sentiment,modelConfig)
    infered_result = myModel.infer()
    db.update_news(infered_result)
