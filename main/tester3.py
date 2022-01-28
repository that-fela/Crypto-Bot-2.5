
from tokenize import PlainToken
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

# SECONDS TESTER FOR ema3ema6ema9

candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '60', 999, False)
#candles1 = historic.get_data_yahoo("ETH-USD", "1h", "7d")
print(len(candles1))
print(candles1[-1].start_time)

#fbv.get_best_sl_tp(candles1, tc.ema3ema6ema9, [1,8], [1,8], 0.0015, 1000)

b= []
t = tc.ema3ema6ema9.init(True, 1000, 0.0015, 0.04, 0.06)
for i in candles1:
    t.add(i)
    b.append(i.close)

r = t.get_result()
print(r[:-1])

print(len(r[4]))
#plt.plot(r[4])
plt.plot(b)
plt.show()
