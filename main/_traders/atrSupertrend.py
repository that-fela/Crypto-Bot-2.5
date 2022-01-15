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
    
    ema1 = 7
    ema2 = 20
    money = 0
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    wins = 0
    losses = 0

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, ema1=7, ema2=20):
        '''uses 5 8 13 ema crossovers for trade. Takes papertrading, startmoney, fee'''
        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.ema1 = ema1
        self.ema2 = ema2
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
        pass

    def update(self):
        '''Updates the trader'''

        # Should work
        # paper trading wins losses 
        if self.in_trade and self.paper_trading:
            if self.in_long:
                if self.candles[self.i].high >= self.buys[-1] * self.percentage[-1]:
                    self.money = self.money * self.percentage - self.money * self.fee
                    self.in_trade = False                    
                    self.wins += 1
                elif self.candles[self.i].low <= self.buys[-1] * (1 + (1 - self.percentage[-1])):
                    self.money = self.money * (1 + (1 - self.percentage[-1])) - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
            
            if not self.in_long:
                if self.candles[self.i].low <= self.sells[-1] * self.percentage[-1]:
                    self.money = self.money * (1 + (1 - self.percentage[-1])) - self.money * self.fee
                    self.in_trade = False
                    self.wins += 1
                elif self.candles[self.i].high >= self.sells[-1] * (1 + (1 - self.percentage)):
                    self.money = self.money * self.percentage - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
        
        # atr
        true_range = []
        cur_tr = []
        atr_t = 20
        atr_20 = []
        atr_upper = []
        atr_lower = []
        atr_multi = 0.45

        if self.i >= 1:
            cur_tr[0] = self.candles[self.i].high - self.candles[self.i].low
            cur_tr[1] = abs(self.candles[self.i].high - self.candles[self.i].close)
            cur_tr[2] = abs(self.candles[self.i].low - self.candles[self.i].close)
            true_range.append(max(true_range))
        
        if self.i >= atr_t + 1:
            atr_20.append((true_range[-atr_t:]) / atr_t)
            atr_upper.append(self.candles[self.i].high + atr_20 * atr_multi)
            atr_lower.append(self.candles[self.i].low - atr_20 * atr_multi)

        if self.i >= atr_t + 1 + 7: 
            emaU = (atr_upper[-1] * (2 / 8)) + (self.atr_upper_ema * (1 - (2 / 8)))
            emaL = (atr_lower[-1] * (2 / 8)) + (self.atr_lower_ema * (1 - (2 / 8)))

            self.atr_upper_ema.append(emaU)
            self.atr_lower_ema.append(emaL)
        else:
            self.atr_upper_ema.append(atr_upper[-1])
            self.atr_lower_ema.append(atr_lower[-1])

        # ema 1
        self.ema1T = self.ema1
        if self.i >= self.ema1T + 1: 
            ema = (self.candles[self.i].close * (2 / (self.ema1T + 1))) + (self.ema1T[-1] * (1 - (2 / (self.ema1T + 1))))
            self.ema1T.append(ema)
        else: self.ema1T.append(self.candles[self.i].close)
        
        # ema 2
        self.ema2T = self.ema2
        if self.i >= self.ema2T + 1: 
            ema = (self.candles[self.i].close * (2 / (self.ema2T + 1))) + (self.ema2T[-1] * (1 - (2 / (self.ema2T + 1))))
            self.ema2T.append(ema)
        else: self.ema2T.append(self.candles[self.i].close)
    

        # trading setup
        if not self.in_trade and self.i > 40:
            if (self.ema1T[-1] > self.ema2T[-1]) and (self.atr_lower_ema[-1] > self.candles[-1].low):
                # BUY
                self.buys.append(self.atr_lower_ema[-1])
                self.in_trade = True 
                self.in_long = True 
                self.percentage.append(self.atr_upper_ema[-1] / self.atr_lower_ema[-1])

            elif (self.ema1T[-1] < self.ema2T[-1]) and (self.atr_upper_ema[-1] < self.candles[-1].upper):
                # SELL
                self.sells.append(self.atr_upper_ema[-1])
                self.in_trade = True 
                self.in_long = False
                self.percentage.append(self.atr_lower_ema[-1] / self.atr_upper_ema[-1])