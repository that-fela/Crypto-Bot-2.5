import yfinance as yf

ticker = yf.Ticker('ETH-USD')

data = ticker.history(interval='5m', period='1mo')
data.to_csv('ethusd5m1mo.csv')