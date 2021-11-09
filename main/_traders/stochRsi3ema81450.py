class init:
    # imported from Crypto bot 1 test_trader
    # WIP DOES NOT WORK FOR LIVE ONLY BACK TEST

    candles = []
    i = -1

    # main declaration 
    ema_8 = []
    ema_14 = []
    ema_50 = []
    Stoch_RSI = []
    k_line = []
    d_line = []
    RSI = []
    RSI_avg_gain = 0
    RSI_avg_loss = 0
    
    tpP = 0.04
    slP =  0.03
    money = 0
    smoney = 0
    buys = []
    sells = []
    in_trade = False
    in_long = True
    trade_atr = 0
    wins = 0
    losses = 0

    def __init__(self, paper_trading=True, start_money=1000, fee=0.0015, tpP=0.05, slP=0.03) -> None:
        '''uses StochRSI 3EMA 8 14 50. Best for 5 min intervals. Uses a Static take profit and stop loss to close trade'''

        self.paper_trading = paper_trading
        self.money = start_money
        self.smoney = start_money
        self.tpP = tpP
        self.slP = slP
        self.fee = 0.0015

    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''

        self.candles.append(candle)
        self.i += 1
        self.update()

    def get_in_trade(self):
        # returns whether or not bot is in trade
        return self.in_trade

    def send_trade(self):
        # sends a trade for live trading
        pass

    def get_result(self):
        '''Returns wins losses money startmoney'''
        return [self.wins, self.losses, self.money, self.smoney]

    def update(self):
        '''Updates the trader'''
        
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
        if self.i >= 7: 
            ema = (self.candles[self.i].close * (2 / 9)) + (self.ema_8[-1] * (1 - (2 / 9)))
            self.ema_8.append(ema)
        else: self.ema_8.append(self.candles[self.i].close)
        if self.i >= 13: 
            ema = (self.candles[self.i].close * (2 / 15)) + (self.ema_14[-1] * (1 - (2 / 15)))
            self.ema_14.append(ema)
        else: self.ema_14.append(self.candles[self.i].close)
        if self.i >= 49: 
            ema = (self.candles[self.i].close * (2 / 51)) + (self.ema_50[-1] * (1 - (2 / 51)))
            self.ema_50.append(ema)
        else: self.ema_50.append(self.candles[self.i].close)

        # step 1 rsi
        if self.i == 14:
            self._gain = 0
            self._loss = 0
            self.last_price = self.candles[self.i-14].close
            for ii in range(self.i-13, self.i):
                if not self.candles[ii].close == self.last_price: 
                    if self.candles[ii].close > self.last_price: 
                        self._gain += (1 - (self.last_price / self.candles[ii].close))
                    else: 
                        self._loss += (1 - (self.candles[ii].close / self.last_price))
                self.last_price = self.candles[ii].close

            self.RSI_avg_gain = self._gain / 14
            self.RSI_avg_loss = self._loss / 14

        # step 2 rsi
        if self.i > 14:
            self._gain = 0
            self._loss = 0
            if not self.candles[self.i].close == self.candles[self.i-1].close:
                if self.candles[self.i].close > self.candles[self.i-1].close:
                    self._gain += (1 - (self.candles[self.i-1].close / self.candles[self.i].close))
                else: 
                    self._loss += (1 - (self.candles[self.i].close / self.candles[self.i-1].close))

                self.RSI_avg_gain = (self.RSI_avg_gain * 13 + self._gain) / 14
                self.RSI_avg_loss = (self.RSI_avg_loss * 13 + self._loss) / 14

        # calculates RSI
        if self.i >= 14:
            self.x = 100 - (100 / (1 + (self.RSI_avg_gain / self.RSI_avg_loss)))
            self.RSI.append(self.x)

        # stochastic RSI
        if len(self.RSI) >= 14:
            self.Stoch_RSI.append((self.RSI[-1] - min(self.RSI[-14:])) / (max(self.RSI[-14:]) - min(self.RSI[-14:])))

        if len(self.Stoch_RSI) >= 3:
            self.sma = sum(self.Stoch_RSI[-3:]) / 3
            self.k_line.append(self.sma)
        
        if len(self.k_line) >= 3:
            self.sma = sum(self.k_line[-3:]) / 3
            self.d_line.append(self.sma)

        self.recent = -1
        self.delay = -2

        # trade logic
        # if not in_trade:
        if not self.in_trade and self.i > 100:
            self.delta_814 = abs(self.ema_8[self.recent] - self.ema_14[self.recent])
            self.delta_1450 = abs(self.ema_14[self.recent] - self.ema_50[self.recent])

            if len(self.d_line) >= 2:
                #if delta_814 >= d814 and delta_1450 >= d1450:
                    if self.ema_8[self.recent] > self.ema_14[self.recent] > self.ema_50[self.recent]:
                        if self.k_line[self.recent] > self.d_line[self.recent] and self.k_line[self.delay] < self.d_line[self.delay]:
                            if self.candles[self.i].close > self.ema_8[self.recent]:
                                self.buys.append(self.candles[self.i].close)
                                self.in_trade = True 
                                self.in_long = True   

                    elif self.ema_8[self.recent] < self.ema_14[self.recent] < self.ema_50[self.recent]:
                        if self.k_line[self.recent] < self.d_line[self.recent] and self.k_line[self.delay] > self.d_line[self.delay]:
                            if self.candles[self.i].close < self.ema_8[self.recent]:
                                self.sells.append(self.candles[self.i].close)
                                self.in_trade = True 
                                self.in_long = False