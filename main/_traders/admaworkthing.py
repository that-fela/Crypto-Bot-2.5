class adamstesttrader:
    def __init__(self) -> None:
        '''Just for me to learn different indicators'''
    
    def add(self, candle):
        '''Adds a new candle. Takes data_types.candle'''
        self.candles.append(candle)
        self.i += 1
        self.update()

    def update(self):
        '''Updates the trader'''
        pass
