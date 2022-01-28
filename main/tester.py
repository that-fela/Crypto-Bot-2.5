
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

# GENERAL TESING OF BYBIT ORDERS

'''
t1 = 23.96
t2 = 23.98
tC = [0, 0]

timestamp = time.strftime('%H:%M')
t = timestamp.split(":")
tC[0] = float(t[0]) 
tC[1] = float(t[1]) / 60
ta = tC[0] + tC[1]

print(t1)
print(t2)
print(ta)

if ta > t1 and ta < t2: 
    print("INTIME")
else: print('NAHSD')

#client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)
#print(client.Symbol.Symbol_get().result()[0]['result'][6])
#print(client.LinearOrder.LinearOrder_new(side="Buy",symbol="ETHUSDT",order_type="Market",qty=0.002,time_in_force="GoodTillCancel",reduce_only=False, close_on_trigger=False).result())
'''
#candles1 = historic.get_data_yahoo('ETH-USD', '1d', '199d')
latest = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '1', 199)
#print(len(candles1))
#print(candles1[len(candles1)-1].close)
#candles2 = historic.get_data('ETH-USD', '5m', '1mo')


#print(type(client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['size']))
'''
t = tc.ema3ema6ema9.init(True, 1000, 0.0015, 0.04, 0.01)
for i in candles1:
    t.add(i)

print(t.get_result())
gr = t.get_results_array()
print(t.conditions_met())

plt.scatter(gr[3], gr[2], color='yellow', marker='o')
plt.scatter(gr[5], gr[4], color='yellow', marker='o')
plt.scatter(gr[7], gr[6], color='green', marker='^')
plt.scatter(gr[9], gr[8], color='red', marker='v')
plt.plot(gr[0], gr[10], linestyle='dashed')
plt.plot(gr[0], gr[11], linestyle='dashed')
plt.plot(gr[0], gr[12], linestyle='dashed')
plt.plot(gr[0], gr[1])
plt.plot(gr[0], gr[13])
plt.show()
'''
t = []
for i in latest:
    t.append(i.close)

plt.plot(t)
plt.show()

#fbv.get_best_sl_tp(candles1, tc.ema3ema6ema9, [1,7], [1,7], 1000)
#fbv.get_best_sl_tp(candles1, tc.ema5ema8ema13, [1,7], [1,7])
#fbv.get_best_sl_tp(candles1, tc.stochRsi3ema81450, [1,7], [1,7])
