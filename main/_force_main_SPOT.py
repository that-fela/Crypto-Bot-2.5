# forces an action if in parameters

from urllib.parse import quote_from_bytes
import historic
import matplotlib.pyplot as plt
from _traders import _trader_controller as tc
import do_trade as DT
import __settings as s
import bybit
from support import networker
import time
import smtplib

# ALL THIS SHIT IS ON SPOT MARKET

try:
    networker.test("UoA-WiFi", False)

    t1 = 11.96 # 11:57:40
    t2 = 11.99 # 11:59:24
    tC = [0, 0]

    timestamp = time.strftime('%H:%M')
    t = timestamp.split(":")
    tC[0] = float(t[0]) 
    tC[1] = float(t[1]) / 60
    ta = tC[0] + tC[1]

    print(str(t1 - ta) + " hours left")

    if ta > t1 and ta < t2:
        print("IN TIME")
        client = bybit.bybit(test=False, api_key=s.apiKey, api_secret=s.apiSecretKey)
        id = 6

        if not DT.in_trade(client, "ETHUSDT"):
            print("Not in trade ... Continuing")

            candles = historic.get_data_bybit_SPOT('ETHUSDT', 'D', 199)
            t = tc.ema3ema6ema9.init(False)
            for i in candles:
                t.add(i)

            # get trade conditions
            cons = t.conditions_met()
            print(DT.get_wallet_ballance_USDT(client)) # wallet
            print(DT.get_ticker_USDT(client, id))   # eth usdt
            qty = round(((DT.get_wallet_ballance_USDT(client) / DT.get_ticker_USDT(client, id)) * 0.9), 4)
            print(qty)
            print(DT.get_ticker_USDT(client, id) * qty)

            if cons[0] == 1:
                # LONG
                if DT.long_tpsl(client, "ETHUSDT", qty, round(1.04 * DT.get_ticker_USDT(client, id), 2), round(0.99 * DT.get_ticker_USDT(client, id), 2), "Market"):
                    print("Buy succesful")
                else:
                    print("BUY NOT COMPLETED")
                    networker.send_email("Sell failed")

            elif cons[0] == 2:
                # SHORT
                if DT.short_tpsl(client, "ETHUSDT", qty, round(0.96 * DT.get_ticker_USDT(client, id), 2), round(1.01 * DT.get_ticker_USDT(client, id), 2), "Market"):
                    print("Sell succesful")
                else:
                    print("SELL NOT COMPLETED")
                    networker.send_email("Sell failed")
                
            elif cons[0] == 0:
                # DO NOTHING
                print("No action")    
        else:
            print("In trade already")
    else:
        print("not in time")

except Exception as e:
    print("Print eroor")
    networker.send_email("ERROR MAIN " + str(e))