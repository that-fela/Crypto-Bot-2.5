from time import monotonic
from turtle import update


class init:
    # uses 3 emas 5 8 13
    # places on positive/negative cross overs

    candles = []
    i = -1

    # main declaration
    atr_upper_ema = []
    atr_lower_ema = []
    percentage = []
    ema1T = []
    ema2T = []
    
    start_after_candles = 50
    ema1 = 7
    ema2 = 20
    money = 0
    monies = []
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    wins = 0
    losses = 0

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, tpsl=0.02, _OTHER=0):
        '''uses 5 8 13 ema crossovers for trade. Takes papertrading, startmoney, fee'''
        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.tpsl = tpsl
        self.fee = fee

    def get_result(self):
        '''Returns wins losses money startmoney ... etc'''

        return [self.wins, self.losses, self.money, self.smoney]

    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''

        self.candles.append(candle)
        self.i += 1
        self.update()

    def conditions_met(self):
        '''returns 0, 1, 2 for none, long, shoty and takeprofit% stoploss%'''
        # return [(0 1 2), tp, sl]
        
        if self.i > self.start_after_candles:
            if (self.ema1T[-2] > self.ema2T[-2]) and (self.atr_lower_ema[-1] > self.candles[-2].low):
                # BUY
                return [1, self.percentage[-1], 2 - self.percentage[-1]]
            elif (self.ema1T[-2] < self.ema2T[-2]) and (self.atr_upper_ema[-1] < self.candles[-2].high):
                # SELL
                return [2, self.percentage[-1], 2 - self.percentage[-1]]
            else:
                return [0, self.percentage[-1], self.percentage[-1]]
        else:
            return [0, self.percentage[-1], self.percentage[-1]]

    def update(self):
        '''Updates the trader'''

        # Should work
        # paper trading wins losses 
        leverage = 1
        self.monies.append(self.money)
        if self.in_trade and self.paper_trading:
            if self.in_long:
                if self.candles[self.i].low <= self.buys[-1] * (1 + (1 - self.percentage[-1])):
                    self.money = self.money + self.money * (1 + (1 - self.percentage[-1])) * leverage - self.money * self.fee * leverage - self.money * leverage
                    self.in_trade = False
                    self.losses += 1
                elif self.candles[self.i].high >= self.buys[-1] * self.percentage[-1]:
                    self.money = self.money + self.money * self.percentage[-1] * leverage - self.money * leverage - self.money * self.fee * leverage
                    self.in_trade =  False                    
                    self.wins += 1
            
            if not self.in_long:
                if self.candles[self.i].high >= self.sells[-1] * (1 + (1 - self.percentage[-1])):
                    self.money = self.money + self.money * self.percentage[-1] * leverage - self.money * self.fee * leverage - self.money * leverage
                    self.in_trade = False
                    self.losses += 1
                elif self.candles[self.i].low <= self.sells[-1] * self.percentage[-1]:
                    self.money = self.money + self.money * (1 + (1 - self.percentage[-1])) * leverage - self.money * self.fee * leverage - self.money * leverage
                    self.in_trade = False
                    self.wins += 1
                    
        # atr_
        true_range = []
        cur_tr = [0, 0, 0]
        atr_t = 20
        atr_ = []
        atr_upper = []
        atr_lower = []
        atr_multi = 0.45

        if self.i >= 1:
            cur_tr[0] = self.candles[self.i].high - self.candles[self.i].low
            cur_tr[1] = abs(self.candles[self.i].high - self.candles[self.i].close)
            cur_tr[2] = abs(self.candles[self.i].low - self.candles[self.i].close)
            true_range.append(max(cur_tr))
        
        if self.i >= atr_t + 1:
            atr_.append(sum(true_range[-atr_t:]) / atr_t)
            atr_upper.append(self.candles[self.i].high + atr_[-1] * atr_multi)
            atr_lower.append(self.candles[self.i].low - atr_[-1] * atr_multi)

            if self.i >= atr_t + 1 + 7: 
                emaU = (atr_upper[-1] * (2 / 8)) + (self.atr_upper_ema[-1] * (1 - (2 / 8)))
                emaL = (atr_lower[-1] * (2 / 8)) + (self.atr_lower_ema[-1] * (1 - (2 / 8)))

                self.atr_upper_ema.append(emaU)
                self.atr_lower_ema.append(emaL)
            else:
                self.atr_upper_ema.append(atr_upper[-1])
                self.atr_lower_ema.append(atr_lower[-1])

        # ema 1
        if self.i >= self.ema1 + 1: 
            ema = (self.candles[self.i].close * (2 / (self.ema1 + 1))) + (self.ema1T[-1] * (1 - (2 / (self.ema1 + 1))))
            self.ema1T.append(ema)
        else: self.ema1T.append(self.candles[self.i].close)
        
        # ema 2
        if self.i >= self.ema2 + 1: 
            ema = (self.candles[self.i].close * (2 / (self.ema2 + 1))) + (self.ema2T[-1] * (1 - (2 / (self.ema2 + 1))))
            self.ema2T.append(ema)
        else: self.ema2T.append(self.candles[self.i].close)
    

        # trading setup
        if not self.in_trade and self.i > self.start_after_candles:
            if (self.ema1T[-2] > self.ema2T[-2]) and (self.atr_lower_ema[-1] > self.candles[-2].low):
                # BUY
                self.buys.append(self.candles[self.i].open)
                self.in_trade = True 
                self.in_long = True 
                self.percentage.append(self.tpsl)

            elif (self.ema1T[-2] < self.ema2T[-2]) and (self.atr_upper_ema[-1] < self.candles[-2].high):
                # SELL
                self.sells.append(self.candles[self.i].open)
                self.in_trade = True 
                self.in_long = False
                self.percentage.append(2 - self.tpsl)