
from audioop import avg
from concurrent.futures import thread
import historic
import matplotlib.pyplot as plt
from _traders import _trader_controller as tc
from data_types import candle
from testing import find_best_values as fbv
import __settings as s
import bybit
import do_trade
import time
import support.networker
import pickle
import json

# ORDER BOOK TESTER

client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)

dp = []
p = []

for i in range(500):
    data = client.Market.Market_orderbook(symbol="ETHUSDT").result()
    price = float(client.Market.Market_symbolInfo().result()[0]['result'][7]['last_price'])

    p.append(price)

    totalBuy = 0
    totalSell = 0

    for i in data[0]["result"]:
        if i["side"] == "Buy":
            totalBuy += float(i["size"])
        if i["side"] == "Sell":
            totalSell += float(i["size"])

    #print(f"Buys : ", totalBuy)
    #print(f"Sells: ", totalSell)
    print(f"", round(totalBuy/totalSell, 2), int(totalBuy), int(totalSell))
    dp.append(totalBuy/totalSell)

    time.sleep(1)

with open('price.txt', 'w') as f:
    f.write(str(p))

with open('bs.txt', 'w') as f:
    f.write(str(dp))