import bybit
import json

client = bybit.bybit(test=True, api_key=apiKey, api_secret=apiSecretKey)
data = client.Kline.Kline_get(symbol="BTCUSD", interval="D", **{'from':1614510000}).result()
for i in data[0]['result']:
    print(i['open'])