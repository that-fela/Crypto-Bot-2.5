class init:
    # uses 3 emas 5 8 13
    # places on positive/negative cross overs

    candles = []
    i = -1

    # main declaration 
    ema_5 = []
    ema_8 = []
    ema_13 = []
    
    tpP = 0.04
    slP =  0.03
    money = 0
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    wins = 0
    losses = 0

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, tpP=0.04, slP=0.03):
        '''uses 5 8 13 ema crossovers for trade. Takes papertrading, startmoney, fee'''
        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.tpP = tpP
        self.slP = slP
        self.fee = fee

    def get_result(self):
        '''Returns wins losses money startmoney ... etc'''

        return [self.wins, self.losses, self.money, self.smoney]

    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''

        self.candles.append(candle)
        self.i += 1
        self.update()

    def update(self):
        '''Updates the trader'''

        # paper trading wins losses 
        if self.in_trade and self.paper_trading:
            if self.in_long:
                if self.candles[self.i].high >= self.buys[-1] + self.buys[-1] * self.tpP:
                    self.money = self.money * (1 + self.tpP) - self.money * self.fee
                    self.in_trade = False
                    self.wins += 1
                elif self.candles[self.i].low <= self.buys[-1] - self.buys[-1] * self.slP:
                    self.money = self.money * (1 - self.slP) - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
            
            if not self.in_long:
                if self.candles[self.i].low <= self.sells[-1] - self.sells[-1] * self.tpP:
                    self.money = self.money * (1 + self.tpP) - self.money * self.fee
                    self.in_trade = False
                    self.wins += 1
                elif self.candles[self.i].high >= self.sells[-1] + self.sells[-1] * self.slP:
                    self.money = self.money * (1 - self.slP) - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
        
        # emas
        #ema 5
        if self.i >= 5: 
            ema = (self.candles[self.i].close * (2 / 6)) + (self.ema_5[-1] * (1 - (2 / 6)))
            self.ema_5.append(ema)
        else: self.ema_5.append(self.candles[self.i].close)
        # ema 8
        if self.i >= 8: 
            ema = (self.candles[self.i].close * (2 / 9)) + (self.ema_8[-1] * (1 - (2 / 9)))
            self.ema_8.append(ema)
        else: self.ema_8.append(self.candles[self.i].close)
        # ema 13
        if self.i >= 13: 
            ema = (self.candles[self.i].close * (2 / 14)) + (self.ema_13[-1] * (1 - (2 / 14)))
            self.ema_13.append(ema)
        else: self.ema_13.append(self.candles[self.i].close)

        # trading setup
        if not self.in_trade and self.i > 26:
            if self.ema_5[-1] > self.ema_8[-1] > self.ema_13[-1]:
                # BUY
                self.buys.append(self.candles[self.i].close)
                self.in_trade = True 
                self.in_long = True 

            elif self.ema_5[-1] < self.ema_8[-1] < self.ema_13[-1]:
                # SELL
                self.sells.append(self.candles[self.i].close)
                self.in_trade = True 
                self.in_long = False