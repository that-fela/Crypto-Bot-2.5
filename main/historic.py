import yfinance as yf
import data_types
import bybit
import __settings as s
from data_types import candle
import time
import datetime

def get_data_yahoo(ticker='ETH-USD', interval='1d', period='3mo'):
    '''Gets historic data. Returns candle of type data_types.candle. Takes ticker, interval, period. Defaults are 'ETH-USD', '1h', '1mo'\n
    valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo\n
    valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max'''
    ticker = yf.Ticker(ticker)
    data = ticker.history(interval=interval, period=period)
    
    candles = []
    for i in range(len(data['Open'])):
        current = data_types.candle()

        #current.start_time = data[dtype='object'][i]
        current.open = data['Open'][i]
        current.close = data['Close'][i]
        current.high = data['High'][i]
        current.low = data['Low'][i]

        candles.append(current)

    return candles

def get_data_bybit_DERIVATIVES(ticker='ETHUSDT', interval='D', period=60, min=False):
    '''Gets historical using ByBit. days https://bybit-exchange.github.io/docs/inverse/#t-orderbook. for unix time stamp https://www.unixtimestamp.com/index.php'''
    client = bybit.bybit(test=True, api_key=s.apiKey, api_secret=s.apiSecretKey)
    fromm = int(time.time()) - period * 24 * 60 * 60
    if min: fromm = int(time.time()) - period * 60
    data = client.LinearKline.LinearKline_get(symbol=ticker, interval=interval, **{'from':fromm}).result()
    
    candles = []
    for i in data[0]['result']:
        current = data_types.candle()

        current.open = float(i['open'])
        current.close = float(i['close'])
        current.high = float(i['high'])
        current.low = float(i['low'])
        current.volume = float(i['volume'])
        current.start_time = int(i['open_time'])

        candles.append(current)

    return candles

# DOES NOT WORK
def get_data_bybit_SPOT(ticker='ETHUSDT', interval='D', period=60):
    '''DOES NOT WORK Gets historical using ByBit. days https://bybit-exchange.github.io/docs/inverse/#t-orderbook. for unix time stamp https://www.unixtimestamp.com/index.php'''
    client = bybit.bybit(test=True, api_key=s.apiKey, api_secret=s.apiSecretKey)
    fromm = int(time.time()) - period * 24 * 60 * 60
    data = client.LinearKline.LinearKline_get(symbol=ticker, interval=interval, **{'from':fromm}).result()
    
    candles = []
    for i in data[0]['result']:
        current = data_types.candle()

        current.open = float(i['open'])
        current.close = float(i['close'])
        current.high = float(i['high'])
        current.low = float(i['low'])
        current.volume = float(i['volume'])
        current.start_time = int(i['open_time'])

        candles.append(current)

    return candles