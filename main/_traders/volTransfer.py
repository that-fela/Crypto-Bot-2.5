from time import monotonic
from turtle import update
import time
from whalealert.whalealert import WhaleAlert
import __settings as s


class init:
    # uses 3 emas 5 8 13
    # places on positive/negative cross overs

    candles = []
    i = -1

    # main declaration
    start_after_candles = 0
    ema1 = 200
    min_amount_usd = 5000000 
    addy2 = "exchange"
    addy1 = "unknown"

    whale = WhaleAlert()
    ema1T = []
    money = 0
    monies = []
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    wins = 0
    losses = 0

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, tp=0.01, sl=0.01):
        '''uses 5 8 13 ema crossovers for trade. Takes papertrading, startmoney, fee'''
        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.tp = tp
        self.sl = sl
        self.fee = fee

    def get_result(self):
        '''Returns wins losses money startmoney ... etc'''

        return [self.wins, self.losses, self.money, self.smoney]

    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''

        self.candles.append(candle)
        self.i += 1
        self.update()

    def get_largest(self, trans):
        TransNum = []
        for i in trans:
            if int(i["amount_usd"]) > self.min_amount_usd:
                if i["blockchain"] == "ethereum":
                    TransNum.append(float(i["amount_usd"]))
        
        id = TransNum.index(max(TransNum))
        
        
                        

    def conditions_met(self):
        '''returns 0, 1, 2 for none, long, shoty and takeprofit% stoploss%'''
        # return [(0 1 2), tp, sl]
        while (True):
            start_time = int(time.time() - (60)) # last 60 seconds
            success, transactions, status = self.whale.get_transactions(start_time, api_key=s.whale_apikey, min_value=self.min_amount_usd)
            
            if len(transactions) <= 99:
                break
            else:
                self.min_amount_usd += 2000000
                print("more than 100 hits ... waiting 7 seconds")
                time.sleep(7)

        if len(transactions) != 0:
            id = self.get_largest(transactions)
        else:
            return [0, 0, 0]
    
    def update(self):
        '''Updates the trader'''

        # Should work
        # paper trading wins losses 
        
        # ema 200
        if self.i >= self.ema1 + 1: 
            ema = (self.candles[self.i].close * (2 / (self.ema1 + 1))) + (self.ema1T[-1] * (1 - (2 / (self.ema1 + 1))))
            self.ema1T.append(ema)
        else: self.ema1T.append(self.candles[self.i].close)

        # trading setup
        # IN CONDITIONS_MET
