import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import matplotlib.pyplot as plt

test_size = 120
pre_day = 30
ma_1 = 7
ma_2 = 14
ma_3 = 21
df = pd.read_csv(f"./data/ADA-USD.csv")

df["Date"]=pd.to_datetime(df.Date,format="mixed").dt.date
df.index=df['Date']

df = df.sort_index(ascending=True, axis=0)
df = pd.DataFrame(df)

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

model=load_model(f"./models/BTC-USD.h5")

# Testing
predict_prices = model.predict(x_test)
predict_prices = scala_y.inverse_transform(predict_prices)

# Ploting the Stat
real_prices = pd.DataFrame(index=range(0, test_size), columns=['Date','Close'])
valid = pd.DataFrame(index=range(0, test_size), columns=['Date','Predictions'])

for i in range(0, len(real_prices)):
    real_prices["Date"][i]=df['Date'][len(df)- i - 1]
    real_prices["Close"][i]=df["Close"][len(df)- i - 1]
    valid["Date"][i]=df['Date'][len(df)- i - 1]

real_price = df[len(df)-test_size:]['Close'].values.reshape(-1, 1)
real_price = np.array(real_price)
real_price = real_price.reshape(real_price.shape[0], 1)

real_prices.index = real_prices['Date']
valid.index = valid['Date']
valid['Predictions'] = np.flip(predict_prices)

plt.plot(real_price, color="red", label=f"Real ADA-USD Prices")
plt.plot(predict_prices, color="blue", label=f"Predicted ADA-USD Prices")
plt.title("ADA-USD Prices")
plt.xlabel("Time")
plt.ylabel("Stock Prices")
plt.ylim(bottom=0)
plt.legend()
plt.show()

x_predict = df[len(df)-pre_day:][cols_x].values.reshape(-1, len(cols_x))
x_predict = scala_x.transform(x_predict)
x_predict = np.array(x_predict)
x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))
prediction = model.predict(x_predict)
prediction = scala_y.inverse_transform(prediction)
print(prediction)
