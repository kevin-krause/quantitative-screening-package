import finnhub
from config import apikey

def get_list(market):
    finnhub_client = finnhub.Client(api_key=apikey)

    stocks = finnhub_client.stock_symbols(market)
    stock_list = []
    for i in stocks:
        stock_list.append(i['symbol'])

    return stock_list