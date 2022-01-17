def get_best_sl_tp(candles, test_trader, range_sl, range_tp, fee=0.0015, start_money=1000):
    '''gets best SL TP Values. Ranges array has to be values * 100'''
    params = []
    vals = []
    returns = []
    for sl in range(range_sl[0], range_sl[1]):
        for tp in range(range_tp[0], range_tp[1]):
            t = test_trader.init(True, start_money, fee, tp/100, sl/100)

            for i in candles:
                t.add(i)
            
            params.append([tp/100, sl/100])
            vals.append(t.get_result()[2])
            returns.append(t.get_result())

            del t

    m = max(vals)
    i = vals.index(m)
    print(params[i])
    print(returns[i])

def get_best_custom_vals(candles, test_trader, var1, var2, fee=0.0015, start_money = 1000):
    '''gets best SL TP Values. Ranges array has to be values * 100'''
    params = []
    vals = []
    returns = []
    for v1 in range(var1[0], var1[1]):
        for v2 in range(var2[0], var2[1]):
            t = test_trader.init(True, start_money, fee, v1, v2)

            for i in candles:
                t.add(i)
            
            params.append([v1, v2])
            vals.append(t.get_result()[2])
            returns.append(t.get_result())

            del t

    m = max(vals)
    i = vals.index(m)
    print(params[i])
    print(returns[i])