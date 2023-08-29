from sklearn.model_selection import GridSearchCV
import xgboost as xgb
# Chart drawing
import plotly as py
import plotly.io as pio
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
import datetime as dt

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

def training_model(token):
    test_size  = 0.15
    valid_size = 0.15
    pre_day = 60

    # Load data for 1year to train 1m interval

    df = pd.read_csv(f"./data_train/{token}_1m.csv")
    df["Datetime"]=pd.to_datetime(df.Datetime,format="mixed")
    df.index=df['Datetime']

    df = df.sort_index(ascending=True, axis=0)
    df = pd.DataFrame(df)
    df.index = range(len(df))

    print(df)
    print("Done Loading Data")

    n = 5
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    sma_1 = 9
    # Process Data
    scala_x = MinMaxScaler(feature_range=(0, 1))
    scala_y = MinMaxScaler(feature_range=(0, 1))
    cols_x = ['Close', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'EMA_{sma_1}', f'SD_{ma_1}', f'SD_{ma_3}', 'MACD', 'MACD_signal',
              f'MiddleBand_{ma_3}', f'UpperBand_{ma_3}', f'LowerBand_{ma_3}', f'RSI_{ma_2}']
    cols_y = ['Close']

    test_split_idx  = int(df.shape[0] * (1-test_size))
    valid_split_idx = int(df.shape[0] * (1-(valid_size+test_size)))

    train_df  = df.loc[:valid_split_idx].copy()
    valid_df  = df.loc[valid_split_idx+1:test_split_idx].copy()
    test_df   = df.loc[test_split_idx+1:].copy()

    # Drop unnecessary columns
    drop_cols = ['Datetime', 'Volume', 'Open', 'Low', 'High', 'Volume', 'Dividends', 'Stock Splits']

    train_df = train_df.drop(columns=drop_cols)
    valid_df = valid_df.drop(columns=drop_cols)
    test_df  = test_df.drop(columns=drop_cols)
    
    # Split into features and labels
    y_train = train_df['Close'].copy()
    X_train = train_df.copy()

    y_valid = valid_df['Close'].copy()
    X_valid = valid_df.copy()

    y_test  = test_df['Close'].copy()
    X_test  = test_df.copy()
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

    eval_set = [(X_train, y_train), (X_valid, y_valid)]
    model = xgb.XGBRegressor()
   
    model.load_model(f"models/{token}_1m_xgboost.json")

    # Calculate and visualize predictions
    y_pred = model.predict(X_test)
    print(f'y_true = {np.array(y_test)[:5]}')
    print(f'y_pred = {y_pred[:5]}')

    print(f'mean_squared_error = {mean_squared_error(y_test, y_pred)}')

    predicted_prices = df.loc[test_split_idx+1:].copy()
    predicted_prices['Close'] = y_pred

    fig = make_subplots(rows=2, cols=1)
    fig.add_trace(go.Scatter(x=df.Datetime, y=df.Close,
                            name='Truth',
                            marker_color='LightSkyBlue'), row=1, col=1)

    fig.add_trace(go.Scatter(x=predicted_prices.Datetime,
                            y=predicted_prices.Close,
                            name='Prediction',
                            marker_color='MediumPurple'), row=1, col=1)

    fig.add_trace(go.Scatter(x=predicted_prices.Datetime,
                            y=y_test,
                            name='Truth',
                            marker_color='LightSkyBlue',
                            showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x=predicted_prices.Datetime,
                            y=y_pred,
                            name='Prediction',
                            marker_color='MediumPurple',
                            showlegend=False), row=2, col=1)

    fig.show()

# symbols = ["BTC-USD", "ETH-USD", "ADA-USD"]
symbols = ["BTC-USD"]

for token in symbols:
    training_model(token)