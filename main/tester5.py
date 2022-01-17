
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

client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)
print("connected")
print(client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['size'])

#candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '60', 200, False)
candles1 = historic.get_data_yahoo("ETH-USD", "1h", "3mo")

print(len(candles1))
print(candles1[-1].start_time)

#fbv.get_best_custom_vals(candles1, tc.atrSupertrend, [1,20], [1,20], 0.0015, 1000)

t = tc.atrSupertrend.init(True, 1000, 0.0015, 2, 3)
for i in candles1:
    t.add(i)

print(t.get_result())

plt.plot(t.monies)
plt.show




