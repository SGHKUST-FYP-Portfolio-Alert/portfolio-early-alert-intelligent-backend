import logging

import coloredlogs
from tqdm import tqdm

from database import database as db
from ext_api import finnhub_wrapper, yahoo_finance

coloredlogs.install(level='WARNING', fmt='%(asctime)s %(name)s[%(process)d] %(funcName)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    
    for counterparty in db.get_counterparties():
        hist = yahoo_finance.fetch_historical_daily_stock_candles(counterparty['symbol'])

        for date, day_range in tqdm(hist.iterrows()):
            doc = {}
            doc['date'] = date
            doc['counterpartyId'] = counterparty['_id']
            doc.update(dict(day_range))

            #optional
            doc['name'] = counterparty['name']
            doc['symbol'] = counterparty['symbol']

            #! no check for overlap saves !
            
            db.counterparty_stock_collection.insert(doc) #way to slow lmao
            # breakpoint()


        print('----------------------------------------------------')

    logger.debug('test')