from yahooquery import Ticker
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
import datetime

class Model:

    def __init__(self, stock) -> None:
        self.stock = stock

    def stock_price(self):
        price = pd.DataFrame(Ticker(f'{self.stock}').history(period="max"))
        price = price.reset_index()
        price = price[['date','open','high', 'low', 'close', 'volume', 'adjclose']]
        return price
    
    def distortions(self):
        df = self.stock_price()
        indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)
        df['bb_bbm'] = indicator_bb.bollinger_mavg()
        df['bb_bbh'] = indicator_bb.bollinger_hband()
        df['bb_bbl'] = indicator_bb.bollinger_lband()
        df['bb_bbw'] = indicator_bb.bollinger_wband()
        return df.drop(df.index[-1])

    def analyze_strategy(self):
        df = dropna(self.distortions())
        
        entry_points = df[(df['close'] < df['bb_bbl']) & (df['bb_bbw'] > df['bb_bbw'].shift(1))]
        exit_points = df[df['close'] > df['bb_bbm']]
        
        position = 0
        initial_balance = 100000  
        balance = initial_balance
        stocks_held = 0
        trade_history = []

        for index, row in df.iterrows():
            if index in entry_points.index:
                if position == 0 and balance > row['close']:
                    stocks_held = balance // row['close']
                    balance -= stocks_held * row['close']
                    position = 1
                    entry_price = row['close']  
                    trade_history.append(('Buy', row['date'], row['close']))
            elif index in exit_points.index:
                if position == 1 and stocks_held > 0:
                    balance += stocks_held * row['close']
                    stocks_held = 0
                    position = 0
                    exit_price = row['close']
                    gain_loss_percentage = ((exit_price - entry_price) / entry_price) * 100
                    trade_history.append(('Sell', row['date'], row['close'], gain_loss_percentage, balance))
        
        if stocks_held > 0:
            balance += stocks_held * df.iloc[-1]['close']

        return balance, trade_history


    def plot(self):
        df = dropna(self.distortions())
        
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['close'], label='Stock Price')
        plt.plot(df.index, df['bb_bbm'], label='Bollinger Middle Band', linestyle='dashed')
        plt.plot(df.index, df['bb_bbh'], label='Bollinger High Band', linestyle='dotted')
        plt.plot(df.index, df['bb_bbl'], label='Bollinger Low Band', linestyle='dotted')
        
        entry_points = df[(df['close'] < df['bb_bbl']) & (df['bb_bbw'] > df['bb_bbw'].shift(1))]
        plt.scatter(entry_points.index, entry_points['close'], color='green', label='Entry Points', marker='^')

        exit_points = df[df['close'] > df['bb_bbm']]
        plt.scatter(exit_points.index, exit_points['close'], color='red', label='Exit Points', marker='v')

        plt.title('Stock Price with Bollinger Bands')
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()


