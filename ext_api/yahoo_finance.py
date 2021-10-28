import logging
import yfinance as yf

logger = logging.getLogger(__name__)

"""Fetches daily stock data of given symbol (defaults to max period from today)
    :Parameters:
        symbol:
            Name of ticker
        period: optional
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        start: optional
            Overrides period
            Download start date string (YYYY-MM-DD) or _datetime.
        end: optional
            Overrides period
            Download end date string (YYYY-MM-DD) or _datetime.
    :Returns:
        hist: pd.DataFrame
            Cols include Date, Open, High, Low, Close, Volume, Dividends, Stock Splits
"""
def fetch_historical_daily_stock_candles(symbol: str, period: str = "max", start: str = None, end: str = None):
    ticker = yf.Ticker(symbol)

    if start != None and end != None:
        hist = ticker.history(start=start, end=end)
    else:
        hist = ticker.history(period=period)

    return hist