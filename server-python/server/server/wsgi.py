"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

application = get_wsgi_application()

# ML registry
from ml.registry import MLRegistry
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
from ml.btc_sticker.btc_rnn import BTCPredictionUsingRNN
from ml.btc_sticker.btc_xgboost import BTCPredictionUsingXGBOOST
try:
    # create ML registry
    registry = MLRegistry()
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
