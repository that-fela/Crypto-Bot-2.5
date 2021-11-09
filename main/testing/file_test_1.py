import yfinance as yf
import pickle


ticker = yf.Ticker('ETH-USD')

data = ticker.history(interval='5m', period='1mo')

candles = []
for i in range(len(data['Open'].values())):
    current = data_types.candle(5*60)

    current.open = data['open'][i]
    current.close = data['close'][i]
    current.high = data['high'][i]
    current.low = data['low'][i]

    candles.append(current)

print(candles[0].open)

with open('test_data.dat', 'wb') as f:
    pickle.dump(candles, f)