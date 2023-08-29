import yfinance as yf
import pandas as pd
import datetime as dt
# Chart drawing
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from sklearn.preprocessing import MinMaxScaler
from utils import powerset
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt

def training_model(token, name, indicator):
    test_size = 300
    pre_day = 60
    indicator.sort()
    # Load data for 1year to train 1m interval
    indicator_str = '_'.join(indicator)
    df = pd.read_csv(f"./data_train/{token}_1m.csv")
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

    x_train = np.array(x_total[:len(x_total)-test_size])
    x_test = np.array(x_total[len(x_total)-test_size:])
    y_train = np.array(y_total[:len(y_total)-test_size])
    y_test = np.array(y_total[len(y_total)-test_size:])

    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    # Build Model

    model = Sequential()
    model.add(
        LSTM(64,return_sequences=True,input_shape = (x_train.shape[1],x_train.shape[2]))) #64 lstm neuron block
    model.add(
        LSTM(64, return_sequences= False))
    model.add(Dense(32))
    model.add(Dense(1))

    model.compile(loss = "mean_squared_error", optimizer = "adam", metrics = ["accuracy"])
    model.fit(x_train, y_train, epochs = 10, batch_size = 10, use_multiprocessing=True)
    token_name = token.lower()
    model.save(f"models/{name}/{token_name}_1m_{name}_{indicator_str}.h5")
    print("Done Training Model")

    # Testing
    predict_prices = model.predict(x_test)
    predict_prices = scala_y.inverse_transform(predict_prices)

    # Ploting the Stat
    real_prices = pd.DataFrame(index=range(0, test_size), columns=['date','close'])
    valid = pd.DataFrame(index=range(0, test_size), columns=['date','Predictions'])
    for i in range(0, len(real_prices)):
        real_prices["date"][i]=df['date'][len(df)- i - 1]
        real_prices["close"][i]=df["close"][len(df)- i - 1]
        valid["date"][i]=df['date'][len(df)- i - 1]

    real_prices.index = real_prices['date']
    valid.index = valid['date']
    valid['Predictions'] = np.flip(predict_prices)

    
    fig = make_subplots(rows=2, cols=1)
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
                            showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x=valid.date,
                            y=valid.Predictions,
                            name='Prediction',
                            marker_color='MediumPurple',
                            showlegend=False), row=2, col=1)

    fig.show()

    # Make Prediction
    x_predict = df[len(df)-pre_day:][cols_x].values.reshape(-1, len(cols_x))
    x_predict = scala_x.transform(x_predict)
    x_predict = np.array(x_predict)
    x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))
    prediction = model.predict(x_predict)
    prediction = scala_y.inverse_transform(prediction)
    print(prediction)

# symbols = ["BTCUSDT", "ETHUSDT", "ETHUSDT"]
symbols = ["BTCUSDT"]
# indicator = ['bb', 'close', 'macd', 'roc', 'rsi', 'sd', 'ma']
indicators = ['bb']
model = ['xgboost', 'rnn', 'lstm']
indicators.sort()
name = "lstm"

r = [x for x in powerset(indicators)]
r.sort()
r.pop(0)
print(len(r))
print(r)

for token in symbols:
    for indicator in r:
        training_model(token, name, indicator)