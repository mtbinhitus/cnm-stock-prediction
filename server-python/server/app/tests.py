from django.test import TestCase
from rest_framework.test import APIClient
from ml.btc_sticker.btc_lstm import BTCPredictionUsingLSTM
from ml.api.binance_websocket import BinanceAPIManager
import ml.api.utils as utils
import datetime as dt
import pandas as pd
import numpy as np
import json

# Create your tests here.

class MLTests(TestCase):
    def test_btc_lstm_algorithm(self):
        # path_to_artifacts = "../research/"
        # df = pd.read_csv(path_to_artifacts + "btc_bars.csv")
        # cols_x = ['date', 'open', 'high', 'low', 'close']
        # x_predict = df[0:30][cols_x]
        # input_data = x_predict.to_json(orient='records')

        # dict= json.loads(input_data)
        # input_data = pd.json_normalize(dict)
        # input_data["date"]=pd.to_datetime(input_data["date"], unit='ns')
        # input_data.index=input_data['date']
        # input_data = input_data.sort_index(ascending=True, axis=0)
        # print(input_data)

        request_data = {"sticker": "BTCUSDT", "model": "LSTM", "indicator": ["Close", "ROC"]}

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

        data_btc = instance.get_historical_klines(symbol='BTCUSDT', interval='1h', startTime=dt.datetime.now() - dt.timedelta(days=3), endTime=dt.datetime.now())
        df_btc = instance.get_dataframe_from_bars(bars=data_btc)
        utils.df_to_csv(df=df_btc, filename="btc_bars")
        input_data = df_btc
        
        my_alg = BTCPredictionUsingLSTM()
        response = my_alg.compute_prediction(input_data)
        print("Date time prediction: ",dt.datetime.fromtimestamp(response['timestamp']))
        print("Price prediction: ", response['prediction'])

        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('btcusdt_lstm_close_ma_poc', response['label'])

class APITests(TestCase):
    def test_predict_view(self):
        client = APIClient()
        input_data = {
            "sticker": "BTCUSDT",
            "model": "LSTM",
            "indicator": ["Close", "POC", "MA"]
        }
        btcsticker_url = "/api/v1/btcsticker/predict"
        response = client.post(btcsticker_url, input_data, format='json')
        print(response)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "btcusdt_lstm_close_ma_poc")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)
