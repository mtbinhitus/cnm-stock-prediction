import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy


class BTCPredictionUsingLSTM:
    pre_day = 30
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    def __init__(self):
        path_to_artifacts = "../research/models/"
        self.model = load_model(path_to_artifacts + "BTC-USD.h5")

    def preprocessing(self, input_data):
        # Process Data
        print("Into process data.....")
        input_data['h-l'] = input_data['high'] - input_data['low']
        input_data['o-c'] = input_data['open'] - input_data['close']

        input_data[f'sma_{self.ma_1}'] = input_data['close'].rolling(window=self.ma_1).mean()
        input_data[f'sma_{self.ma_2}'] = input_data['close'].rolling(window=self.ma_2).mean()
        input_data[f'sma_{self.ma_3}'] = input_data['close'].rolling(window=self.ma_3).mean()
        input_data[f'sd_{self.ma_1}'] = input_data['close'].rolling(window=self.ma_1).std()
        input_data[f'sd_{self.ma_3}'] = input_data['close'].rolling(window=self.ma_3).std()
        input_data.dropna(inplace=True)

        print(input_data)

        self.scala_x = MinMaxScaler(feature_range=(0, 1))
        self.scala_y = MinMaxScaler(feature_range=(0, 1))
        cols_x = ['h-l', 'o-c', f'sma_{self.ma_1}', f'sma_{self.ma_2}', f'sma_{self.ma_3}', f'sd_{self.ma_1}', f'sd_{self.ma_3}']
        cols_y = ['close']
        scaled_data_x = self.scala_x.fit_transform(input_data[cols_x].values.reshape(-1, len(cols_x)))
        scaled_data_y = self.scala_y.fit_transform(input_data[cols_y].values.reshape(-1, len(cols_y)))

        x_predict = input_data[len(input_data)- 1 - self.pre_day: len(input_data) - 1][cols_x].values.reshape(-1, len(cols_x))
        x_predict = self.scala_x.transform(x_predict)

        x_predict = np.array(x_predict)
        x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))
        
        print("End pre-processing...")
        print(x_predict.shape)
        
        return x_predict

    def predict(self, input_data):
        prediction = self.model.predict(input_data)
        prediction = self.scala_y.inverse_transform(prediction)
        return prediction

    def postprocessing(self, timestamp, prediction):
        return {"prediction": round(prediction.astype('float64'), 2), "timestamp": np.int64(timestamp / 1000.0),"label": "btcusdt_lstm_close_ma_poc", "status": "OK"}

    def compute_prediction(self, input_data):
        try:
            print("Try to compute prediction......")
            timestamp = input_data['timestamp'][len(input_data) - 1]
            
            input_data = self.preprocessing(input_data)

            print("Make prediction....")
            prediction = self.predict(input_data)  # 1 mẫu
            print("Return result....!")
            prediction = self.postprocessing(timestamp, prediction[0][0])
        except Exception as e:
            print(e)
            return {"status": "Error", "message": str(e)}

        return prediction
