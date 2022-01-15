
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

#candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '5', 200, True)
candles1 = historic.get_data_yahoo("ETH-USD", "30m", "1mo")

print(len(candles1))
print(candles1[-1].start_time)

#fbv.get_best_custom_vals(candles1, tc.atrSupertrend, [1,50], [1,50], 0.0015, 1000)

t = tc.atrSupertrend.init(True, 1000, 0.0015, 7, 20)
for i in candles1:
    t.add(i)

print(t.get_result())




