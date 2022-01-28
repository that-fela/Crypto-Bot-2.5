
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

# TESTER FOR VOLTRANSFER

#client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)
#print("connected")
#print(client.LinearPositions.LinearPositions_myPosition(symbol="ETHUSDT").result()[0]['result'][0]['position_value'])

#candles1 = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '60', 5, False)
candles1 = historic.get_data_yahoo("ETH-USD", "30m", "30d")

print(len(candles1))
print(candles1[-1].start_time)

fbv.get_best_sl_tp(candles1, tc.atrConstant, [1,10], [1,2], 0.0015, 1000)



