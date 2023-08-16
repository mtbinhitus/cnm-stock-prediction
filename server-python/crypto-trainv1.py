import yfinance as yf
import pandas as pd
import datetime as dt

from sklearn.preprocessing import MinMaxScaler

import numpy as np

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy

import matplotlib.pyplot as plt

def training_model(token):
    start = '01/06/2009'
    end = dt.datetime.now().strftime("%d/%m/%Y")
    test_size = 60
    pre_day = 30

    # Load data
    Ticker = yf.Ticker(token)
    df = Ticker.history(period="max")
    df = pd.DataFrame(df)

    # df=pd.read_csv("BTC-USD.csv")
    # df.head()

    # df["Date"]=pd.to_datetime(df.Date, format='mixed', utc=True)
    # df.index=df['Date']
    print(df)

    df['H-L'] = df['High'] - df['Low']
    df['O-C'] = df['Open'] - df['Close']
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    df[f'SMA_{ma_1}'] = df['Close'].rolling(window=ma_1).mean()
    df[f'SMA_{ma_2}'] = df['Close'].rolling(window=ma_2).mean()
    df[f'SMA_{ma_3}'] = df['Close'].rolling(window=ma_3).mean()
    df[f'SD_{ma_1}'] = df['Close'].rolling(window=ma_1).std()
    df[f'SD_{ma_3}'] = df['Close'].rolling(window=ma_3).std()
    df.dropna(inplace=True)

    df.to_csv(f"{token}.csv")
    print("Done Loading Data")

    # Process Data
    scala_x = MinMaxScaler(feature_range=(0, 1))
    scala_y = MinMaxScaler(feature_range=(0, 1))
    cols_x = ['H-L', 'O-C', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'SD_{ma_1}', f'SD_{ma_3}']
    cols_y = ['Close']
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

    model.add(LSTM(units=60, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60, return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(units=60))
    model.add(Dropout(0.2))
    model.add(Dense(units=len(cols_y)))

    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train, y_train, epochs=120, steps_per_epoch=40, use_multiprocessing=True)
    model.save(f"./models/{token}.h5")
    print("Done Training Model")

    # Testing
    predict_prices = model.predict(x_test)
    predict_prices = scala_y.inverse_transform(predict_prices)

    # Ploting the Stat
    real_price = df[len(df)-test_size:]['Close'].values.reshape(-1, 1)
    real_price = np.array(real_price)
    real_price = real_price.reshape(real_price.shape[0], 1)


    plt.plot(real_price, color="red", label=f"Real {token} Prices")
    plt.plot(predict_prices, color="blue", label=f"Predicted {token} Prices")
    plt.title(f"{token} Prices")
    plt.xlabel("Time")
    plt.ylabel("Stock Prices")
    plt.ylim(bottom=0)
    plt.legend()
    plt.show()

    # Make Prediction
    x_predict = df[len(df)-pre_day:][cols_x].values.reshape(-1, len(cols_x))
    x_predict = scala_x.transform(x_predict)
    x_predict = np.array(x_predict)
    x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))
    prediction = model.predict(x_predict)
    prediction = scala_y.inverse_transform(prediction)
    print(prediction)

symbols = ["BTC-USD", "ETH-USD", "ADA-USD"]

for token in symbols:
    training_model(token)