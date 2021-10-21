
import logging

import coloredlogs

from ext_api import finnhub_wrapper

coloredlogs.install(level='WARNING', fmt='%(asctime)s %(name)s[%(process)d] %(funcName)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

finnhub_wrapper.fetch_historical_daily_stock_candles('AAPL')
# finnhub_wrapper.fetch_historical_daily_stock_candles('MSFT')

logger.debug('test')
