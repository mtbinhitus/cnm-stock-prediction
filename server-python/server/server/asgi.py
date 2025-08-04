"""
ASGI config for server project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import app.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            app.routing.websocket_urlpatterns 
        )
    )
})

from threading import Thread
from ml.api.binance_websocket import BinanceAPIManager
import ml.api.utils as utils
import datetime as dt
import pandas as pd
import asyncio
import signal

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
            data_btc = instance.get_historical_klines(symbol='BTCUSDT', interval='1m', startTime=dt.datetime.now() - dt.timedelta(days=7), endTime=dt.datetime.now())
            df_btc = instance.get_dataframe_from_bars(bars=data_btc)
            utils.df_to_csv(df=df_btc, filename="btc_bars")
            
            try:
                loop = asyncio.get_event_loop()
                # for sig in (signal.SIGINT, signal.SIGTERM):
                #     loop.add_signal_handler(sig, loop.stop)
                    
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

import sys
# ML registry
from ml.registry import MLRegistry
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
from ml.btc_sticker.btc_rnn import BTCPredictionUsingRNN
from ml.btc_sticker.btc_xgboost import BTCPredictionUsingXGBOOST
# create ML registry
registry = MLRegistry()

# only run this code when runserver, daphne, uvicorn server
# skip if migrate or makemigrations
if any(cmd in sys.argv[0] or cmd in " ".join(sys.argv) for cmd in ["runserver", "daphne", "uvicorn"]):
    try:
        # BTCLSTM
        lstm = BTCPredictionUsingLSTM()
        # add to ML registry
        print("Import Model")
        registry.add_algorithm(endpoint_name="btcsticker",
                                algorithm_object=lstm,
                                algorithm_name="btcusdt_lstm",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Binh Mai",
                                algorithm_description="LSTM model to predict close price of BTCUSDT.")
        
        # BTCRNN
        rnn = BTCPredictionUsingRNN()
        registry.add_algorithm(endpoint_name="btcsticker",
                                algorithm_object=rnn,
                                algorithm_name="btcusdt_rnn",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Binh Mai",
                                algorithm_description="RNN model to predict close price of BTCUSDT.")
        
        # BTCXGBoost
        xgboost = BTCPredictionUsingXGBOOST()
        registry.add_algorithm(endpoint_name="btcsticker",
                                algorithm_object=xgboost,
                                algorithm_name="btcusdt_xgboost",
                                algorithm_status="production",
                                algorithm_version="0.0.1",
                                owner="Binh Mai",
                                algorithm_description="XGBoost model to predict close price of BTCUSDT.")
    except Exception as e:
        print("Exception while loading the algorithms to the registry,", str(e))

    btc_socket = RealTimeThread()
    btc_socket.start()
