from sklearn.model_selection import GridSearchCV
import xgboost as xgb
# Chart drawing
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt
from utils import powerset
from sklearn.preprocessing import MinMaxScaler

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM, SimpleRNN
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import Accuracy
from tensorflow.keras import optimizers
from tensorflow.keras import backend as K
import matplotlib.pyplot as plt
from xgboost import plot_importance, plot_tree
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, GridSearchCV

def rmse(y_true, y_pred):
    return K.sqrt(K.mean(K.square(y_pred - y_true), axis=-1))


def mda(y_true, y_pred, t=12):
    d = K.equal(K.sign(y_true[t: ] - y_true[:-t]),
                K.sign(y_pred[t: ] - y_pred[:-t]))
    return K.mean(K.cast(d, K.floatx()))

def training_model(token, name, indicator):
    test_size  = 0.2
    pre_day = 60
    indicator.sort()
    # Load data for 1year to train 1m interval
    indicator_str = '_'.join(indicator)
    df = pd.read_csv(f"./data_train/{token}_1m_xgboost.csv")
    df["date"]=pd.to_datetime(df.date,format="mixed")
    df.index=df['date']

    df = df.sort_index(ascending=True, axis=0)
    df = pd.DataFrame(df)
    df.index = range(len(df))
    df['close_forecast'] = df['close'].shift(-1, axis=0)
    # df.dropna(inplace=True)
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

    # cols_x = ['close', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'EMA_{sma_1}', f'SD_{ma_1}', f'SD_{ma_3}', 'macd', 'macd_signal',
    #           f'middleband_{ma_3}', f'upperband_{ma_3}', f'lowerband_{ma_3}', f'RSI_{ma_2}']
    # indicator = ['bb', 'close', 'macd', 'roc', 'rsi', 'sd', 'ma']
    cols_x = ['close', 'close_forecast']
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
        

    test_split_idx  = int(df.shape[0] * (1-test_size))

    train_df  = df.loc[:test_split_idx].copy()
    test_df   = df.loc[test_split_idx+1:].copy()

    train_df = train_df[cols_x]
    test_df  = test_df[cols_x]
    
    # Split into features and labels
    y_train = train_df['close_forecast'].copy()
    X_train = train_df.drop(columns=['close_forecast'])

    y_test  = test_df['close_forecast'].copy()
    X_test  = test_df.drop(columns=['close_forecast'])
    X_test.info()
    X_train.info()

    # Fine-tune XGBoostRegressor
    parameters = {
    'n_estimators': [100, 200, 300, 400],
    'learning_rate': [0.001, 0.005, 0.01, 0.05],
    'max_depth': [8, 10, 12, 15],
    'gamma': [0.001, 0.005, 0.01, 0.02],
    'random_state': [42]
    }

    # eval_set = [(X_train, y_train), (X_valid, y_valid)]
    # model = xgb.XGBRegressor(objective='reg:squarederror')
    # clf = GridSearchCV(model, parameters)

    # clf.fit(X_train, y_train, eval_set=eval_set, verbose=False)

    # print(f'Best params: {clf.best_params_}')
    # print(f'Best validation score = {clf.best_score_}')

    # model = xgb.XGBRegressor(**clf.best_params_, objective='reg:squarederror')
    # model.fit(X_train, y_train, eval_set=eval_set, verbose=False)

    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=42, booster='gbtree')
    model.fit(X_train, y_train)
    plot_importance(model)
    token_name = token.lower()
    model.save_model(f"models/{name}/{token_name}_1m_{name}_{indicator_str}.json")

    # Calculate and visualize predictions
    y_pred = model.predict(X_test)
    print(f'y_true = {np.array(y_test)[-5:]}')
    print(f'y_pred = {y_pred[-5:]}')

    print(f'mean_squared_error = {mean_squared_error(y_test[:-1], y_pred[:-1])}')

    predicted_prices = df.loc[test_split_idx+1:].copy()
    predicted_prices['close'] = y_pred

    # fig = make_subplots(rows=2, cols=1)
    # fig.add_trace(go.Scatter(x=df.date, y=df.close,
    #                         name='Truth',
    #                         marker_color='LightSkyBlue'), row=1, col=1)

    # fig.add_trace(go.Scatter(x=predicted_prices.date,
    #                         y=predicted_prices.close,
    #                         name='Prediction',
    #                         marker_color='MediumPurple'), row=1, col=1)

    # fig.add_trace(go.Scatter(x=predicted_prices.date,
    #                         y=y_test,
    #                         name='Truth',
    #                         marker_color='LightSkyBlue',
    #                         showlegend=False), row=2, col=1)

    # fig.add_trace(go.Scatter(x=predicted_prices.date,
    #                         y=y_pred,
    #                         name='Prediction',
    #                         marker_color='MediumPurple',
    #                         showlegend=False), row=2, col=1)

    # fig.show()

    # Make Prediction
    next_day = test_df.copy().drop('close_forecast', axis='columns').tail(2)
    next_day_pred = model.predict(next_day)
    next_day_close = next_day_pred[0]
    print(next_day_close)

# symbols = ["BTC-USD", "ETH-USD", "ADA-USD"]
symbols = ["BTCUSDT"]
# indicator = ['bb', 'close', 'macd', 'roc', 'rsi', 'sd', 'ma']
indicators = ['bb', 'close', 'macd', 'roc', 'rsi', 'sd', 'ma']
model = ['xgboost', 'rnn', 'lstm']
indicators.sort()
name = "xgboost"

r = [x for x in powerset(indicators)]
r.sort()
r.pop(0)
print(len(r))
print(r)

for token in symbols:
    for indicator in r:
        training_model(token, name, indicator)