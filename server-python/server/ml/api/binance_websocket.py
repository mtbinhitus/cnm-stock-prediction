from ml.api import utils
import os
from time import sleep
from binance import ThreadedWebsocketManager, AsyncClient, BinanceSocketManager
from binance.client import Client
import pandas as pd
from datetime import datetime
import datetime as dt
import numpy as np

class BinanceAPIManager():
    def __init__(self, api_key, api_secret, api_endpoint):
        self.api_key = utils.get_env_variable(api_key)
        self.api_secret = utils.get_env_variable(api_secret)
        self.client = Client(api_key, api_secret)
        self.client.API_URL = utils.get_env_variable(api_endpoint)

        # init and start the WebSocket
        self.bsm = ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)

    async def task_btcusdt_socket(self):
        client = await AsyncClient.create(self.api_key, self.api_secret)
        bm = BinanceSocketManager(client)
        ds = bm.kline_socket(symbol='BTCUSDT', interval= AsyncClient.KLINE_INTERVAL_1MINUTE)

        async with ds as kline_socket:
            while True:
                res = await kline_socket.recv()
                await self.handle_socket_message(res)

    async def handle_socket_message(self, msg):
        # define how to process incoming WebSocket messages
        df = pd.read_csv("./btc_bars.csv")
        df['date'] = [datetime.fromtimestamp(x / 1000.0) for x in df.timestamp]
        df.set_index('date', inplace=True)
        price = {}
        # print(msg)
        if msg['e'] != 'error':
            price['date'] = dt.datetime.fromtimestamp(msg['k']['t']/1000.0)
            price['timestamp'] = msg['k']['t']
            price['open'] = msg['k']['o']
            price['high'] = msg['k']['h']
            price['low'] = msg['k']['l']
            price['close'] = msg['k']['c']
            price = pd.Series(price)
            # print(price)
            df.loc[price['date']] = price
            utils.df_to_csv(df=df, filename="btc_bars")
            # print(df[len(df)-2:])
        else:
            price['error'] = True

    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    def get_earliest_valid_timestamp(self, symbol, interval):
        # get timestamp of earliest date data is available
        timestamp = self.client._get_earliest_valid_timestamp(symbol, interval)
  
        return timestamp
    
    # valid intervals - 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d, 1w, 1M
    def get_historical_klines(self, symbol='BTCUSDT', interval='1m', startTime=None, endTime=None, limit=None):
        if startTime is not None:
            startTime_UTC = str(int(startTime.timestamp() * 1000))
        else: startTime_UTC = None
        if endTime is not None:
            endTime_UTC = str(int(endTime.timestamp() * 1000))
        else: endTime_UTC = None
        print("Start time: ", startTime)
        print("End time: ", endTime)

        # request historical candle (or klines) data, limit maximum is 1000 candle
        if limit is not None:
            bars = self.client.get_historical_klines(symbol, interval, start_str=startTime_UTC, end_str=endTime_UTC, limit=limit)
        else: bars = self.client.get_historical_klines(symbol, interval, start_str=startTime_UTC, end_str=endTime_UTC)
        # delete unwanted data - just keep date, open, high, low, close
        for line in bars:
            del line[5:]
        
        return bars
    
    def get_dataframe_from_bars(self, bars):
        # create a Pandas DataFrame and export to CSV
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close'])
        df['open']=df.open.replace('', np.nan).astype('float64')
        df['high']=df.high.replace('', np.nan).astype('float64')
        df['low']=df.low.replace('', np.nan).astype('float64')
        df['close']=df.close.replace('', np.nan).astype('float64')
        df['date'] = [datetime.fromtimestamp(x / 1000.0) for x in df.timestamp]
        df.set_index('date', inplace=True)

        return df
    
    # start websocket
    def start_websocket(self):
        self.bsm.start()
    
    # stop websocket
    def stop_websocket(self):
        self.bsm.stop()
    
    # subscribe to a stream
    def subscribe_to_a_stream(self, symbol):
        self.bsm.start_kline_socket(callback=self.handle_socket_message, symbol=symbol)


# Stream real-time data from websocket
# instance.start_websocket()
# instance.subscribe_to_a_stream(symbol='BTCUSDT')
# utils.countdown(10)
# instance.stop_websocket()