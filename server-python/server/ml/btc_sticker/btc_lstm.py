import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy

import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class BTCPredictionUsingLSTM:
    n = 5
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    ema_1 = 9
    pre_day = 60
    def __init__(self):
        path_to_artifacts = "../research/models/lstm/"
        self.model = load_model(path_to_artifacts + "btcusdt_1m_lstm_close.h5")

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
        for i in indicator:
            if(i == 'bb'):
                cols_x.extend([f'middleband_{ma_3}', f'upperband_{ma_3}', f'lowerband_{ma_3}'])
            elif (i == 'close'):
                cols_x.append('close')
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

    def postprocessing(self, timestamp, prediction, label):
        return {"prediction": round(prediction.astype('float64'), 2), "time": timestamp,"label": label, "status": "OK"}

    def compute_prediction(self, input_data, indicator):
        try:
            print("Try to compute prediction......")
            timestamp = input_data['time'][len(input_data) - 1]
            indicator.sort()
            indicator_str = '_'.join(indicator)

            self.path_to_artifacts = "../research/models/lstm/" + f"btcusdt_1m_lstm_{indicator_str}.h5"
            self.path_to_artifacts = self.path_to_artifacts.lower()
            self.model = load_model(self.path_to_artifacts)
            input_data = self.preprocessing(input_data, indicator)

            print("Make prediction....")
            prediction = self.predict(input_data)  # 1 mẫu
            print("Return result....!")
            label = 'lstm_' + indicator_str
            prediction = self.postprocessing(timestamp, prediction[0][0], label=label)
        except Exception as e:
            if("No file or directory found at" in str(e)):
                return {"status": "Error", "message": "Model is not available!"}
            print(e)
            return {"status": "Error", "message": str(e)}

        return prediction

    def visualize(self, indicator):
        indicator.sort()
        indicator_str = '_'.join(indicator)
        path_to_artifacts = "../research/models/lstm/" + f"btcusdt_1m_lstm_{indicator_str}.h5"
        path_to_artifacts = path_to_artifacts.lower()
        model = load_model(path_to_artifacts)

        test_size  = 0.3
        pre_day = 60
        # Load data for 1year to train 1m interval
        indicator_str = '_'.join(indicator)
        df = pd.read_csv(f"../research/data_train/BTCUSDT_1m.csv")
        df["date"]=pd.to_datetime(df.date,format="mixed")
        df.index=df['date']

        df = df.sort_index(ascending=True, axis=0)
        df = pd.DataFrame(df)
        
        print(df)
        print("Done Loading Data")

        n = 5
        ma_1 = 7
        ma_2 = 14
        ma_3 = 21
        ema_1 = 9
        # Process Data
        scala_x = MinMaxScaler(feature_range=(0, 1))
        scala_y = MinMaxScaler(feature_range=(0, 1))
        # cols_x = ['close', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'SD_{ma_1}', f'SD_{ma_3}',
        #           f'MiddleBand_{ma_3}', f'UpperBand_{ma_3}', f'LowerBand_{ma_3}', f'RSI_{ma_2}']
        # indicator = ['bb', 'close', 'macd', 'roc', 'rsi', 'sd', 'ma']
        cols_x = []
        for i in indicator:
            if(i == 'bb'):
                    cols_x.extend([f'middleband_{ma_3}', f'upperband_{ma_3}', f'lowerband_{ma_3}'])
            elif (i == 'close'):
                cols_x.append('close')
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

        cols_y = ['close']
        scaled_data_x = scala_x.fit_transform(df[cols_x].values.reshape(-1, len(cols_x)))
        scaled_data_y = scala_y.fit_transform(df[cols_y].values.reshape(-1, len(cols_y)))

        x_total = []
        y_total = []

        for i in range(pre_day, len(df)):
            x_total.append(scaled_data_x[i-pre_day:i])
            y_total.append(scaled_data_y[i])

        test_split_idx  = int(df.shape[0] * (1-test_size))

        x_train = np.array(x_total[:test_split_idx])
        x_test = np.array(x_total[test_split_idx + 1:])
        y_train = np.array(y_total[:test_split_idx])
        y_test = np.array(y_total[test_split_idx + 1:])

        print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

        # Calculate and visualize predictions
        predict_prices = model.predict(x_test)
        predict_prices = scala_y.inverse_transform(predict_prices)

    # Ploting the Stat
        real_prices = pd.DataFrame(index=range(0, len(x_test)), columns=['date','close'])
        valid = pd.DataFrame(index=range(0, len(x_test)), columns=['date','Predictions'])
        for i in range(0, len(real_prices)):
            real_prices["date"][i]=df['date'][len(df)- i - 1]
            real_prices["close"][i]=df["close"][len(df)- i - 1]
            valid["date"][i]=df['date'][len(df)- i - 1]

        real_prices.index = real_prices['date']
        valid.index = valid['date']
        valid['Predictions'] = np.flip(predict_prices)

        fig = make_subplots(rows=3, cols=1, subplot_titles=("Overview", "RSI & MACD", "Prediction"))
        
        fig.add_trace(go.Scatter(x=df.date, y=df.close,
                                name='Truth',
                                marker_color='LightSkyBlue'), row=1, col=1)

        fig.add_trace(go.Scatter(x=valid.date,
                                y=valid.Predictions,
                                name='Prediction',
                                marker_color='MediumPurple'), row=1, col=1)

        fig.add_trace(go.Scatter(x=valid.date,
                                y=real_prices.close,
                                name='Truth',
                                marker_color='LightSkyBlue',
                                showlegend=False), row=3, col=1)

        fig.add_trace(go.Scatter(x=valid.date,
                                y=valid.Predictions,
                                name='Prediction',
                                marker_color='MediumPurple',
                                showlegend=False), row=3, col=1)
        
        fig.add_trace(go.Scatter(x=df.date, y=df.sma_7, name='SMA 7'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df.sma_14, name='SMA 14'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df.sma_21, name='SMA 21'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df.ema_9, name='EMA 9'), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df.rsi_14, name='RSI 14'),  row=2, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df['macd'], name='MACD'), row=2, col=1)
        fig.add_trace(go.Scatter(x=df.date, y=df['macd_signal'], name='Signal line'), row=2, col=1)
        fig.add_trace(go.Scatter(x = df['date'],
                         y = df['upperband_21'],
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         name = 'upper band',
                         opacity = 0.2),
              row = 1, col = 1)
        fig.add_trace(go.Scatter(x = df['date'],
                         y = df['lowerband_21'],
                         line_color = 'gray',
                         line = {'dash': 'dash'},
                         fill = 'tonexty',
                         name = 'lower band',
                         opacity = 0.2),
              row = 1, col = 1)
        fig.update_layout(height=1400, autosize=True)
        # fig.show()
        return fig
