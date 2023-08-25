"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_asgi_application()

# ML registry
from ml.registry import MLRegistry
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
try:
    # create ML registry
    registry = MLRegistry()
    # BTCLSTM
    rf = BTCPredictionUsingLSTM()
    # add to ML registry
    registry.add_algorithm(endpoint_name="btcsticker",
                            algorithm_object=rf,
                            algorithm_name="btcusdt_lstm_close_ma_poc",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="Binh Mai",
                            algorithm_description="LSTM using ROC, MA, SD to predict 1h candle price of BTCUSDT.")
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))


from threading import Thread
from ml.api.binance_websocket import BinanceAPIManager
import ml.api.utils as utils
import datetime as dt
import pandas as pd
import asyncio

class RealTimeThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)

    def run(self):
        global df_btc
        # draw data over 1000 cây nến 1m :))

        try:
            print('Thread running')
            api_key = 'BINANCE_API_KEY'
            api_secret = 'BINANCE_API_SECRET_KEY'
            api_endpoint = 'BINANCE_API_ENDPOINT'

            instance = BinanceAPIManager(api_key, api_secret, api_endpoint)
            data_btc = instance.get_historical_klines(symbol='BTCUSDT', interval='1m', startTime=dt.datetime.now() - dt.timedelta(days=2), endTime=dt.datetime.now())
            df_btc = instance.get_dataframe_from_bars(bars=data_btc)
            utils.df_to_csv(df=df_btc, filename="btc_bars")
            
            try:
                loop = asyncio.get_event_loop()
                asyncio.ensure_future(instance.task_btcusdt_socket())
                loop.run_forever()
            except KeyboardInterrupt:
                pass
            finally:
                print("Closing Loop")
                loop.close()

        except Exception as e:
            print("Exception while loading data from binance,", str(e))
    
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

btc_socket = RealTimeThread()
btc_socket.start()
