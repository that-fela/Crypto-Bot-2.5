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

# ALL THIS SHIT IS ON DERIVATIVES MARKET

try:
    networker.test("SPARK-QC5E56", False)

    tC = [0, 0]

    timestamp = time.strftime('%H:%M')
    t = timestamp.split(":")

    tC[0] = float(t[0]) 
    tC[1] = float(t[1]) / 60
    ta = tC[0] + tC[1]

    # check every hour
    for t1 in range(0, 23):
        t2 = t1 + 0.02

        if ta > t1 and ta < t2:
            print("IN TIME")
            client = bybit.bybit(test=True, api_key=s.apiKey, api_secret=s.apiSecretKey)
            id = 7

            if not DT.in_trade(client, "ETHUSDT"):
                print("Not in trade ... Continuing")

                # 60min
                candles = historic.get_data_bybit_DERIVATIVES('ETHUSDT', '60', 199)
                t = tc.ema3ema6ema9.init(False)
                for i in candles:
                    t.add(i)

                # get trade conditions
                cons = t.conditions_met()
                print("Wallet in USDT: ", DT.get_wallet_ballance_USDT(client)) # wallet
                print("Price of BTC in USDT: ", DT.get_ticker_USDT(client, id))   # eth usdt
                qty = round(((DT.get_wallet_ballance_USDT(client) / DT.get_ticker_USDT(client, id)) * 0.9), 3)
                print("Amount of ETH: ", qty)
                print("Order value in USDT: ", (DT.get_ticker_USDT(client, id) * qty))
                print("Print condition: ", cons)

                if cons[0] == 1:
                    # LONG
                    if DT.long_tpsl(client, "ETHUSDT", qty, round(1.04 * DT.get_ticker_USDT(client, id), 2), round(0.94 * DT.get_ticker_USDT(client, id), 2), "Market"):
                        print("Buy succesful")
                    else:
                        print("BUY NOT COMPLETED")
                        networker.send_email("Buy failed")

                elif cons[0] == 2:
                    # SHORT
                    if DT.short_tpsl(client, "ETHUSDT", qty, round(0.96 * DT.get_ticker_USDT(client, id), 2), round(1.06 * DT.get_ticker_USDT(client, id), 2), "Market"):
                        print("Sell succesful")
                    else:
                        print("SELL NOT COMPLETED")
                        networker.send_email("Sell failed")
                    
                elif cons[0] == 0:
                    # DO NOTHING
                    print("No action")    
            else:
                print("In trade already")

except Exception as e:
    print("Print error")
    print(str(e))
    networker.send_email("ERROR MAIN " + str(e))
