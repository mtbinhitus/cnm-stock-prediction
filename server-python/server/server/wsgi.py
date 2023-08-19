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
try:
    # create ML registry
    registry = MLRegistry()
    # BTCLSTM
    rf = BTCPredictionUsingLSTM()
    # add to ML registry
    registry.add_algorithm(endpoint_name="btcsticker",
                            algorithm_object=rf,
                            algorithm_name="LSTM using ROC, MA, SD",
                            algorithm_status="production",
                            algorithm_version="0.0.1",
                            owner="Binh Mai",
                            algorithm_description="LSTM using ROC, MA, SD to predict 1h candle price of BTCUSDT.")
except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))