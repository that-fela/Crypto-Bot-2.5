from os import truncate
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
import random



latest = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '120', 120*199, True)

pl = []
print(latest[-1].start_time)
for i in latest:
    pl.append(i.close)

t = tc.ema3ema6ema9.init(True, 1000, 0.0015, 0.03, 0.06)
for i in latest:
    t.add(i)

print(t.get_result())
gr = t.get_results_array()

fbv.get_best_sl_tp(latest, tc.ema3ema6ema9, [1,7], [1,7], 1000)

plt.plot(pl)
plt.show()

r = []
for i in range(10):
    x = random.randint(200, 1000)
    latest = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '120', 120*x, True)
    t = tc.ema3ema6ema9.init(True, 1000, 0.0015, 0.02, 0.03)
    for i in latest:
        t.add(i)
    r.append(t.get_result()[2])

av = 0
for i in r:
    av += i
print(av/len(r))
print(r)