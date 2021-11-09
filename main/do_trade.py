# makes trading
from contextlib import closing
from logging import fatal
from time import time
from typing import Collection
import bybit


# initilisation
#client = bybit.bybit(test=test, api_key=s.apiKey, api_secret=s.apiSecretKey)

# following is all examples:
# get current wallet money of USDT
#wallet_money = float(client.Wallet.Wallet_getBalance(coin="USDT").result()[0]['result']['USDT']['available_balance'])
#print(wallet_money)

# getting current price of commodity (ETH-USDT)
#coin = 5 # 0 = BTCUSD, 1 = ETHUSD, 2 = EOSUSD, 3 = XRPUSD, 4 = BTCUSDT, 5 = ETHUSDT, ...
#price = float(client.Market.Market_symbolInfo().result()[0]['result'][coin]['last_price'])
#print(price)

# example of an order
# client.LinearOrder.LinearOrder_new(side="Buy", symbol="ETHUSDT", order_type="Market", qty="'Quantity in BTC'", time_in_force="GoodTillCancel", take_profit=, stop_loss=, reduce_only=True, close_on_trigger=False).result()
def get_BTCUSDT(client):
    btcprice = float(client.Market.Market_symbolInfo().result()[0]['result'][4]['last_price'])
    return btcprice

def get_ticker_USDT(client, ticker):
    '''5 BTCUSDT, 6 ETHUSDT'''
    price = float(client.Market.Market_symbolInfo().result()[0]['result'][ticker]['last_price'])
    return price

def get_wallet_ballance_USDT(client):
    wallet_money = float(client.Wallet.Wallet_getBalance(coin="USDT").result()[0]['result']['USDT']['available_balance'])
    return wallet_money

def in_trade(client, symbol="ETHUSDT"):
    size = client.LinearPositions.LinearPositions_myPosition(symbol=symbol).result()[0]['result'][0]['size']
    if size == 0:
        return False
    elif size != 0:
        return True
    else:
        return 0

def long_tpsl(client, symbol, quantity, tp, sl, type="Market"):
    '''client.obj, Symbol, current price, quantity in ETH, takeprofit, sl, order type'''
    ret = client.LinearOrder.LinearOrder_new(side="Buy", symbol=symbol, order_type=type, qty=quantity, time_in_force="GoodTillCancel", take_profit=tp, stop_loss=sl, reduce_only=False, close_on_trigger=False).result()
    print(ret)
    if ret[0]['ret_code'] == 0:
        return True
    else:
        return False

def short_tpsl(client, symbol, quantity, tp, sl, type="Market"):
    '''client.obj, Symbol, current price, quantity in ETH, takeprofit, sl, order type'''
    ret = client.LinearOrder.LinearOrder_new(side="Sell", symbol=symbol, order_type=type, qty=quantity, time_in_force="GoodTillCancel", take_profit=tp, stop_loss=sl, reduce_only=False, close_on_trigger=False).result()
    print(ret)
    if ret[0]['ret_code'] == 0:
        return True
    else:
        return False