from matplotlib.pyplot import tick_params


class init:
    # uses 3 emas 3 6 9
    # places on positive/negative cross overs

    candles = []
    i = -1

    # main declaration 
    ema_3 = []
    ema_6 = []
    ema_9 = []
    
    start_after_candles = 31
    tpP = 0.0
    slP =  0.0
    money = 0
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    wins = 0
    losses = 0

    takeprofit = []
    tp_time= []
    stoploss = []
    sl_time = []
    buy_time = []
    sell_time = []

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, tpP=0.04, slP=0.01):
        '''uses 3 6 9 ema crossovers for trade. Best 1d Takes papertrading, startmoney, fee'''
        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.tpP = tpP
        self.slP = slP
        self.fee = fee

    def get_results_array(self):
        low = []
        high = []
        inter = [i for i in range(0, self.i+1)]
        for i in self.candles:
            low.append(i.low)
            high.append(i.high)
        
        return [inter, low, self.buys, self.buy_time, self.sells, self.sell_time, self.takeprofit, self.tp_time, self.stoploss, self.sl_time, self.ema_3, self.ema_6, self.ema_9, high]

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

        if self.i > self.start_after_candles:
            if self.ema_3[-1] > self.ema_6[-1] > self.ema_9[-1]:
                # BUY
                return [1, self.tpP, self.slP]

            elif self.ema_3[-1] < self.ema_6[-1] < self.ema_9[-1]:
                # SELL
                return [2, self.tpP, self.slP]
            else:
                return [0, self.tpP, self.slP]
        else:
            return [0, self.tpP, self. slP]

    def update(self):
        '''Updates the trader'''

        # paper trading wins losses 
        if self.in_trade and self.paper_trading:
            if self.in_long:
                if self.candles[self.i].high >= self.buys[-1] + self.buys[-1] * self.tpP:
                    self.money = self.money * (1 + self.tpP) - self.money * self.fee
                    self.in_trade = False
                    self.wins += 1
                    self.takeprofit.append(self.candles[self.i].high)
                    self.tp_time.append(self.i)

                elif self.candles[self.i].low <= self.buys[-1] - self.buys[-1] * self.slP:
                    self.money = self.money * (1 - self.slP) - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
                    self.stoploss.append(self.candles[self.i].low)
                    self.sl_time.append(self.i)
            
            if not self.in_long:
                if self.candles[self.i].low <= self.sells[-1] - self.sells[-1] * self.tpP:
                    self.money = self.money * (1 + self.tpP) - self.money * self.fee
                    self.in_trade = False
                    self.wins += 1
                    self.takeprofit.append(self.candles[self.i].low)
                    self.tp_time.append(self.i)

                elif self.candles[self.i].high >= self.sells[-1] + self.sells[-1] * self.slP:
                    self.money = self.money * (1 - self.slP) - self.money * self.fee
                    self.in_trade = False
                    self.losses += 1
                    self.stoploss.append(self.candles[self.i].high)
                    self.sl_time.append(self.i)

        # emas
        #ema 3
        if self.i >= 3: 
            ema = (self.candles[self.i].close * (2 / 4)) + (self.ema_3[-1] * (1 - (2 / 4)))
            self.ema_3.append(ema)
        else: self.ema_3.append(self.candles[self.i].close)
        # ema 6
        if self.i >= 6: 
            ema = (self.candles[self.i].close * (2 / 7)) + (self.ema_6[-1] * (1 - (2 / 7)))
            self.ema_6.append(ema)
        else: self.ema_6.append(self.candles[self.i].close)
        # ema 9
        if self.i >= 9: 
            ema = (self.candles[self.i].close * (2 / 10)) + (self.ema_9[-1] * (1 - (2 / 10)))
            self.ema_9.append(ema)
        else: self.ema_9.append(self.candles[self.i].close)

        # trading setup
        if not self.in_trade and self.i > self.start_after_candles:
            if self.ema_3[-1] > self.ema_6[-1] > self.ema_9[-1]:
                # BUY
                self.buys.append(self.candles[self.i].close)
                self.in_trade = True 
                self.in_long = True 
                self.buy_time.append(self.i)

            elif self.ema_3[-1] < self.ema_6[-1] < self.ema_9[-1]:
                # SELL
                self.sells.append(self.candles[self.i].close)
                self.in_trade = True 
                self.in_long = False
                self.sell_time.append(self.i)