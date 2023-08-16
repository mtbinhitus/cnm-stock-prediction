import utils
import os
from time import sleep
from binance import ThreadedWebsocketManager
from binance.client import Client
import pandas as pd

class BinanceAPIManager():
    def __init__(self, api_key, api_secret, api_endpoint):
        self.api_key = utils.get_env_variable(api_key)
        self.api_secret = utils.get_env_variable(api_secret)
        self.client = Client(api_key, api_secret)
        self.client.API_URL = utils.get_env_variable(api_endpoint)

        # init and start the WebSocket
        self.bsm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)

    def handle_socket_message(self, msg):
        # define how to process incoming WebSocket messages
        price = {'error':False}
        print(msg)
        if msg['e'] != 'error':
            print(msg['c'])
            price['last'] = msg['c']
            price['bid'] = msg['b']
            price['last'] = msg['a']
            price['error'] = False
        else:
            price['error'] = True

    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    def get_earliest_valid_timestamp(self, symbol, interval):
        # get timestamp of earliest date data is available
        timestamp = self.client._get_earliest_valid_timestamp(symbol, interval)
        print(timestamp)
        return timestamp
    
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    def get_historical_klines(self, symbol, interval):
        timestamp = self.client._get_earliest_valid_timestamp(symbol, interval)
        # request historical candle (or klines) data, limit maximum is 1000 candle
        bars = self.client.get_historical_klines(symbol, interval, timestamp)
        
        # delete unwanted data - just keep date, open, high, low, close
        for line in bars:
            del line[5:]
        
        print(bars)
        return bars
    
    def get_dataframe_from_bars(self, bars):
        # create a Pandas DataFrame and export to CSV
        df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
        df.set_index('date', inplace=True)
        print(df.head())
        return df
    
    # start websocket
    def start_websocket(self):
        self.bsm.start()
    
    # stop websocket
    def stop_websocket(self):
        self.bsm.stop()
    
    # subscribe to a stream
    def subscribe_to_a_stream(self, symbol):
        self.bsm.start_symbol_ticker_socket(callback=self.handle_socket_message, symbol=symbol)




# test load env var
value = utils.get_env_variable("BINANCE_API_SECRET_KEY")
if value == None:
    print("checkpoint")
else:
    print(value)

# Load historical data from binance api\
api_key = 'BINANCE_API_KEY'
api_secret = 'BINANCE_API_SECRET_KEY'
api_endpoint = 'BINANCE_API_ENDPOINT'

instance = BinanceAPIManager(api_key, api_secret, api_endpoint)

data_btc = instance.get_historical_klines(symbol='BTCUSDT', interval='1d')
df_btc = instance.get_dataframe_from_bars(bars=data_btc)
utils.df_to_csv(df=df_btc)

# Stream real-time data from websocket
# instance.start_websocket()
# instance.subscribe_to_a_stream(symbol='BTCUSDT')
# utils.countdown(10)
# instance.stop_websocket()