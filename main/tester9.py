
from audioop import avg
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

# TESTER FOR ATREMA

#client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)
#print("connected")
#print(client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['position_value'])

#candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '60', 5, False)
candles1 = historic.get_data_yahoo("ETH-USD", "30m", "1mo")

print(len(candles1))
print(candles1[-1].start_time)

fbv.get_best_custom_vals(candles1, tc.atrEma, [1,300], [1,2], 0.0015, 1000)
'''
t = tc.atrEma.init(True, 100, 0.0015)
for i in candles1:
    t.add(i)

r = t.get_result()
print(r)
print(max(t.percentage))
print("Win rate %: " + str(r[0]/(r[1]+r[0])*100))
print("Trades per day: " + str((r[0]+r[1])/30))

plt.plot(t.monies)
plt.yscale("log")
plt.show()
'''

