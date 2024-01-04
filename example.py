from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
from backtesting.test import SMA, GOOG
import talib as ta


class RSI(Strategy):
    n1 = 14
    ovb = 70
    ovs = 30
    ma_length = 20
    def init(self):
        close = self.data.Close
        self.rsi = self.I(ta.RSI, close, self.n1)
        self.ma = self.I(ta.EMA, close, self.ma_length)

    def next(self):
        if self.rsi < self.ovs and self.data.Open > self.ma:
            self.buy()
        elif self.rsi > self.ovb and self.data.Open < self.ma :
            self.sell()

dji = pd.read_csv('./data/us30_m15_from_2021_to_oct_2023.csv')

# map column name
dji.rename(columns={'open':'Open', 'high':'High', 'low':'Low', 'close':'Close', 'tick_volume':'Volume'}, inplace=True)

print(dji.head())
print(GOOG.head())


bt = Backtest(dji, RSI,
              cash=10000000, commission=.002, 
              exclusive_orders=True)

output = bt.run()
bt.plot()

    
print('::::::::::::::::::::::::::::::::::::::::::::::::::::')
print(output)
print('::::::::::::::::::::::::::::::::::::::::::::::::::::')
print(output._trades)
print('::::::::::::::::::::::::::::::::::::::::::::::::::::')
