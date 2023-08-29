import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import xgboost as xgb
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, SimpleRNN
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy


class BTCPredictionUsingXGBOOST:
    n = 5
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    ema_1 = 9
    pre_day = 60
    def __init__(self):
        path_to_artifacts = "../research/models/xgboost/"
        self.model = xgb.XGBRegressor()
        self.model.load_model(path_to_artifacts + "btcusdt_1m_xgboost_close.json")

    def preprocessing(self, input_data, indicator):
        # Process Data
        print("Into process data.....")
        # Calculate ROC
        n = 5
        N =input_data['close'].diff(n)
        D =input_data['close'].shift(n)
        input_data[f'roc_{n}'] = N/D
        # Using 7 14 21 sma and 7 21 sd for short term 1m interval 
        ma_1 = 7
        ma_2 = 14
        ma_3 = 21
        ema_1 = 9
        # Simple Moving Avarage
        input_data[f'sma_{ma_1}'] = input_data['close'].rolling(window=ma_1).mean()
        input_data[f'sma_{ma_2}'] = input_data['close'].rolling(window=ma_2).mean()
        input_data[f'sma_{ma_3}'] = input_data['close'].rolling(window=ma_3).mean()

        # Exponential Moving Average
        input_data[f'ema_{ema_1}'] = input_data['close'].ewm(ema_1).mean().shift()

        # Standard Deviation
        input_data[f'sd_{ma_1}'] = input_data['close'].rolling(window=ma_1).std()
        input_data[f'sd_{ma_3}'] = input_data['close'].rolling(window=ma_3).std()

        # MCAD
        EMA_12 = pd.Series(input_data['close'].ewm(span=12, min_periods=12).mean())
        EMA_26 = pd.Series(input_data['close'].ewm(span=26, min_periods=26).mean())
        input_data['macd'] = pd.Series(EMA_12 - EMA_26)
        input_data['macd_signal'] = pd.Series(input_data.macd.ewm(span=9, min_periods=9).mean())
        
        # Compute the Bollinger Bands using the 21-kline Moving average
        input_data[f'middleband_{ma_3}'] = input_data[f'sma_{ma_3}']
        input_data[f'upperband_{ma_3}'] = input_data[f'sma_{ma_3}'] + (2 * input_data[f'sd_{ma_3}']) 
        input_data[f'lowerband_{ma_3}'] = input_data[f'sma_{ma_3}'] - (2 * input_data[f'sd_{ma_3}'])

        # Relative Strength Index
        close_delta = input_data['close'].diff()
        up = close_delta.clip(lower=0)
        down = -1 * close_delta.clip(upper=0)
        ma_up = up.ewm(com = ma_2 - 1, adjust=True, min_periods = ma_2).mean()
        ma_down = down.ewm(com = ma_2 - 1, adjust=True, min_periods = ma_2).mean()
        rsi = ma_up / ma_down
        rsi = 100 - (100/(1 + rsi))
        input_data[f'rsi_{ma_2}'] = rsi

        input_data.dropna(inplace=True)

        print(input_data)

        self.scala_x = MinMaxScaler(feature_range=(0, 1))
        self.scala_y = MinMaxScaler(feature_range=(0, 1))
        n = 5
        ma_1 = 7
        ma_2 = 14
        ma_3 = 21
        ema_1 = 9
        cols_x = []
        cols_x = ['close']
        for i in indicator:
            if(i == 'close'):
                cols_x.extend(['open', 'high', 'low'])
            if(i == 'bb'):
                cols_x.extend([f'middleband_{ma_3}', f'upperband_{ma_3}', f'lowerband_{ma_3}'])
            elif (i == 'macd'):
                cols_x.extend(['macd', 'macd_signal'])
            elif (i == 'roc'):
                cols_x.append(f'roc_{n}')
            elif (i == 'rsi'):
                cols_x.append(f'rsi_{ma_2}')
            elif (i == 'sd'):
                cols_x.extend([f'sd_{ma_1}', f'sd_{ma_3}'])
            elif (i == 'ma'):
                cols_x.extend([f'sma_{ma_1}', f'sma_{ma_2}', f'sma_{ma_3}', f'ema_{ema_1}'])


        test_df = input_data[cols_x].copy().drop('close', axis='columns')
        x_predict = test_df.tail(1)
        
        print("End pre-processing...")
        print(x_predict.shape)
        
        return x_predict

    def predict(self, input_data):
        prediction = self.model.predict(input_data)

        return prediction

    def postprocessing(self, timestamp, prediction, label):
        return {"prediction": round(prediction.astype('float64'), 2), "time": timestamp,"label": label, "status": "OK"}

    def compute_prediction(self, input_data, indicator):
        try:
            print("Try to compute prediction......")
            timestamp = input_data['time'][len(input_data) - 1]
            indicator.sort()
            indicator_str = '_'.join(indicator)

            self.path_to_artifacts = "../research/models/xgboost/" + f"btcusdt_1m_xgboost_{indicator_str}.json"
            self.path_to_artifacts = self.path_to_artifacts.lower()
            self.model.load_model(self.path_to_artifacts)
            input_data = self.preprocessing(input_data, indicator)

            print("Make prediction....")
            prediction = self.predict(input_data)  # 1 mẫu
            print("Return result....!")
            label = 'xgboost_' + indicator_str
            prediction = self.postprocessing(timestamp, prediction[0], label=label)
        except Exception as e:
            print(e)
            return {"status": "Error", "message": str(e)}

        return prediction
