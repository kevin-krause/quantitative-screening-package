from yahooquery import Ticker
import pandas as pd
from ta.utils import dropna
from ta.volatility import BollingerBands
import matplotlib.pyplot as plt
import datetime

petr = Ticker("PETR4.SA")
df =pd.DataFrame(petr.history(period="max"))

class Model:

    def __init__(self, stock) -> None:
        self.stock = stock

    def stock_price(self):
        """
        Pegar dados de preço do fechamento diário 
        das empresas brasileiras
        """
        price = pd.DataFrame(Ticker(f'{self.stock}.SA').history(period="max"))

        price = price.reset_index()

        price = price[['date','open','high', 'low', 'close', 'volume', 'adjclose']]
        
        
        return price
    
    def distortions(self):
        df = self.stock_price()

        indicator_bb = BollingerBands(close=df["close"], window=20, window_dev=2)

        # Add Bollinger Bands features
        df['bb_bbm'] = indicator_bb.bollinger_mavg()
        df['bb_bbh'] = indicator_bb.bollinger_hband()
        df['bb_bbl'] = indicator_bb.bollinger_lband()

        # # Add Bollinger Band high indicator
        # df['bb_bbhi'] = indicator_bb.bollinger_hband_indicator()

        # # Add Bollinger Band low indicator
        # df['bb_bbli'] = indicator_bb.bollinger_lband_indicator()

        # # Add Width Size Bollinger Bands
        # df['bb_bbw'] = indicator_bb.bollinger_wband()

        # # Add Percentage Bollinger Bands
        # df['bb_bbp'] = indicator_bb.bollinger_pband()

        return df.drop(df.index[-1])

    def plot(self):
        df = dropna(self.distortions())
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['date'], df['close'], label='Stock Price')
        plt.plot(df['date'], df['bb_bbm'], label='Bollinger Middle Band', linestyle='dashed')
        plt.plot(df['date'], df['bb_bbh'], label='Bollinger High Band', linestyle='dotted')
        plt.plot(df['date'], df['bb_bbl'], label='Bollinger Low Band', linestyle='dotted')
        
        # # Entry points: When the price crosses below the lower band and the width is expanding
        # entry_points = df[(df['close'] < df['bb_bbl']) & (df['bb_bbw'] > df['bb_bbw'].shift(1))]
        # plt.scatter(entry_points.index, entry_points['close'], color='green', label='Entry Points', marker='^')

        # # Exit points: When the price crosses above the middle band
        # exit_points = df[df['close'] > df['bb_bbm']]
        # plt.scatter(exit_points.index, exit_points['close'], color='red', label='Exit Points', marker='v')

        plt.title('Stock Price with Bollinger Bands')
        plt.xlabel('date')
        plt.ylabel('price')
        plt.legend()
        plt.show()

# print(Model('PETR4').stock_price())
Model('PETR4').plot()