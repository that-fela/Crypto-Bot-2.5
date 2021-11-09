import historic
import traders

candles = historic.get_data()

t1 = traders.test_trader()
for i in candles:
    t1.add(i)

 

