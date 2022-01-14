
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

#candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '5', 200, True)
candles1 = historic.get_data_yahoo("ETH-USD", "5m", "1mo")
print(len(candles1))
print(candles1[-1].start_time)

fbv.get_best_sl_tp(candles1, tc.ema3ema6ema9, [1,10], [1,10], 0.0015, 1000)

t = tc.ema10ema41support.init(True, 1000, 0.002, 0.04, 0.02)
for i in candles1:
    t.add(i)

print(t.get_result())




