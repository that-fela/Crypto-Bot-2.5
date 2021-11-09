# data types

# candle object
class candle:
    prices = []
    times = []
    
    time_frame = 0
    start_time = 0
    end_time = 0

    high = 0
    low = 0
    open = 0
    close = 0
    volume = 0 

    candle_id = 0

    def __init__(self, time_frame=0) -> None:
        '''Intialises Candle. Takes time frame of the candle in seconds (leave blank if not needed ie back testing)'''
        self.time_frame = time_frame
        self.prices = []
        self.times = []
    
    def update(self):
        '''Updates function. No reason to be called'''
        self.open = self.prices[0]
        self.close = self.prices[-1]
        
        self.high = max(self.prices)
        self.low = min(self.prices)

    def add_data(self, price, time, candle_id=0):
        '''Adds Data. Takes the current price, current time, and ID (not needed)'''
        self.prices.append(price)
        self.times.append(time)
        self.candle_id = candle_id
        
        self.start_time = self.times[0]
        self.end_time = self.start_time + self.time_frame

        self.update()
    