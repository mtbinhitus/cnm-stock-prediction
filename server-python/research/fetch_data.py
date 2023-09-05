import yfinance as yf
import pandas as pd
import datetime as dt
import numpy as np
from binance_websocket import BinanceAPIManager

def fetch_data_yfinance(token, period, interval, xgboost=False):
    # Load data for 7 days to train 1m interval
    # Ticker = yf.Ticker(token)
    # df = Ticker.history(period=period, interval=interval)
    api_key = 'BINANCE_API_KEY'
    api_secret = 'BINANCE_API_SECRET_KEY'
    api_endpoint = 'BINANCE_API_ENDPOINT'

    instance = BinanceAPIManager(api_key, api_secret, api_endpoint)
    df = instance.get_historical_klines(symbol=token, interval=interval, startTime=dt.datetime.now() - dt.timedelta(days=period), endTime=dt.datetime.now())
    df = instance.get_dataframe_from_bars(bars=df)

    df = pd.DataFrame(df)
    print(df)

    # Calculate ROC
    n = 5
    N =df['close'].diff(n)
    D =df['close'].shift(n)
    df[f'roc_{n}'] = N/D
    # Using 7 14 21 sma and 7 21 sd for short term 1m interval 
    ma_1 = 7
    ma_2 = 14
    ma_3 = 21
    ema_1 = 9
    # Simple Moving Avarage
    df[f'sma_{ma_1}'] = df['close'].rolling(window=ma_1).mean()
    df[f'sma_{ma_2}'] = df['close'].rolling(window=ma_2).mean()
    df[f'sma_{ma_3}'] = df['close'].rolling(window=ma_3).mean()

    # Exponential Moving Average
    df[f'ema_{ema_1}'] = df['close'].ewm(ema_1).mean().shift()

    # Standard Deviation
    df[f'sd_{ma_1}'] = df['close'].rolling(window=ma_1).std()
    df[f'sd_{ma_3}'] = df['close'].rolling(window=ma_3).std()

    # MCAD
    EMA_12 = pd.Series(df['close'].ewm(span=12, min_periods=12).mean())
    EMA_26 = pd.Series(df['close'].ewm(span=26, min_periods=26).mean())
    df['macd'] = pd.Series(EMA_12 - EMA_26)
    df['macd_signal'] = pd.Series(df.macd.ewm(span=9, min_periods=9).mean())
    
    # Compute the Bollinger Bands using the 21-kline Moving average
    df[f'middleband_{ma_3}'] = df[f'sma_{ma_3}']
    df[f'upperband_{ma_3}'] = df[f'sma_{ma_3}'] + (2 * df[f'sd_{ma_3}']) 
    df[f'lowerband_{ma_3}'] = df[f'sma_{ma_3}'] - (2 * df[f'sd_{ma_3}'])

    # Relative Strength Index
    close_delta = df['close'].diff()
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    ma_up = up.ewm(com = ma_2 - 1, adjust=True, min_periods = ma_2).mean()
    ma_down = down.ewm(com = ma_2 - 1, adjust=True, min_periods = ma_2).mean()
    rsi = ma_up / ma_down
    rsi = 100 - (100/(1 + rsi))
    df[f'rsi_{ma_2}'] = rsi

    # Save to csv
    df.dropna(inplace=True)
    if xgboost is True:
        df.to_csv(f"data_train/{token}_1m_xgboost.csv")
    else: df.to_csv(f"data_train/{token}_1m.csv")
    print("Done Loading Data")

fetch_data_yfinance('BTCUSDT', period=7, interval="1m")
fetch_data_yfinance('BTCUSDT', period=5, interval="1m", xgboost=True)