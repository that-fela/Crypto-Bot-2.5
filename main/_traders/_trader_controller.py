from _traders import atrEma, volTransfer, atrConstant, ema10ema41support, ema5ema8ema13, stochRsi3ema81450, ema3ema6ema9, admaworkthing, atrSupertrend

class test_trader:
    candles = []

    def __init__(self, time_frame_self, time_frame_candle, start_money=1000, fee=0.0015):
        '''descrption of how the trader works. Time frame of Trader (seconds). Time frame of candles (seconds). Takes Fee'''
        pass

    def get_result(self):
        '''Returns wins losses money startmoney ... etc'''
        pass

    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''
        self.candles.append(candle)
        self.update()
        pass

    def update(self):
        '''Updates the trader'''
        pass



