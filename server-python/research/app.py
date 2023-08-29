import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import numpy as np

def load_and_predict(token):
    df = pd.read_csv(f"./data_train/{token}_1m.csv")

    df["Date"]=pd.to_datetime(df.Date,format="mixed")
    df.index=df['Date']

    df = df.sort_index(ascending=True, axis=0)
    df = pd.DataFrame(df)
    print(df)
    # Process Data
    scala_x = MinMaxScaler(feature_range=(0, 1))
    scala_y = MinMaxScaler(feature_range=(0, 1))
    cols_x = ['Close', f'SMA_{ma_1}', f'SMA_{ma_2}', f'SMA_{ma_3}', f'SD_{ma_1}', f'SD_{ma_3}',
              f'MiddleBand_{ma_3}', f'UpperBand_{ma_3}', f'LowerBand_{ma_3}', f'RSI_{ma_2}']
    cols_y = ['Close']
    scaled_data_x = scala_x.fit_transform(df[cols_x].values.reshape(-1, len(cols_x)))
    scaled_data_y = scala_y.fit_transform(df[cols_y].values.reshape(-1, len(cols_y)))

    x_total = []
    y_total = []

    for i in range(pre_day, len(df)):
        x_total.append(scaled_data_x[i-pre_day:i])
        y_total.append(scaled_data_y[i])
    print(df[len(x_total)-test_size:])
    x_train = np.array(x_total[:len(x_total)-test_size])
    x_test = np.array(x_total[len(x_total)-test_size:])
    y_train = np.array(y_total[:len(y_total)-test_size])
    y_test = np.array(y_total[len(y_total)-test_size:])

    print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)

    model=load_model(f"models/{token}_1m_lstm_lstm_close_poc_ma_sd_rsi_bb.h5")

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

    real_prices.index = real_prices['Date']
    valid.index = valid['Date']
    valid['Predictions'] = np.flip(predict_prices)

    x_predict = df[len(df)-pre_day-1:len(df)-1][cols_x].values.reshape(-1, len(cols_x))
    x_predict = scala_x.transform(x_predict)
    x_predict = np.array(x_predict)
    x_predict = x_predict.reshape(1, x_predict.shape[0], len(cols_x))
 
    print(x_predict.shape)
    prediction = model.predict(x_predict)
    prediction = scala_y.inverse_transform(prediction)
    print(prediction)

    x_predict = np.array(x_total[len(x_total)-1:])
    print(x_predict.shape)
    prediction = model.predict(x_predict)
    prediction = scala_y.inverse_transform(prediction)
    print(prediction)

    return real_prices, valid, prediction

symbols = ["BTC-USD", "ETH-USD", "ADA-USD"]
test_size = 120
pre_day = 60
ma_1 = 7
ma_2 = 14
ma_3 = 21

app = dash.Dash()
server = app.server
rp_btc, valid_btc, lastest_btc = load_and_predict(symbols[0])
# rp_eth, valid_eth, lastest_eth = load_and_predict(symbols[1])
# rp_ada, valid_ada, lastest_ada = load_and_predict(symbols[2])

app.layout = html.Div([
   
    html.H1("Crypto Price Analysis Dashboard", style={"textAlign": "center"}),
   
    dcc.Tabs(id="tabs", children=[
       
        dcc.Tab(label='BTC-USD Crypto Data',children=[
			html.Div([
				html.H2("Actual closing price",style={"textAlign": "center"}),
                html.H3(f"Price prediction for tomorrow: {lastest_btc[0][0]:.2f} USD",style={"textAlign": "center"}),
				dcc.Graph(
					id="Actual Data BTC",
					figure={
						"data":[
							go.Scatter(
								x=rp_btc.index,
								y=rp_btc["Close"],
								mode='markers'
							)

						],
						"layout":go.Layout(
							title='scatter plot',
							xaxis={'title':'Date'},
							yaxis={'title':'Closing Rate'}
						)
					}

				),
				html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
				dcc.Graph(
					id="Predicted Data BTC",
					figure={
						"data":[
							go.Scatter(
								x=valid_btc.index,
								y=valid_btc["Predictions"],
								mode='markers'
							)

						],
						"layout":go.Layout(
							title='scatter plot',
							xaxis={'title':'Date'},
							yaxis={'title':'Closing Rate'}
						)
					}

				)				
			])        		


        ]),
    #    dcc.Tab(label='ETH-USD Crypto Data',children=[
	# 		html.Div([
	# 			html.H2("Actual closing price",style={"textAlign": "center"}),
    #             html.H3(f"Price prediction for tomorrow: {lastest_eth[0][0]:.2f} USD",style={"textAlign": "center"}),
	# 			dcc.Graph(
	# 				id="Actual Data ETH",
	# 				figure={
	# 					"data":[
	# 						go.Scatter(
	# 							x=rp_eth.index,
	# 							y=rp_eth["Close"],
	# 							mode='markers'
	# 						)

	# 					],
	# 					"layout":go.Layout(
	# 						title='scatter plot',
	# 						xaxis={'title':'Date'},
	# 						yaxis={'title':'Closing Rate'}
	# 					)
	# 				}

	# 			),
	# 			html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
	# 			dcc.Graph(
	# 				id="Predicted Data ETH",
	# 				figure={
	# 					"data":[
	# 						go.Scatter(
	# 							x=valid_eth.index,
	# 							y=valid_eth["Predictions"],
	# 							mode='markers'
	# 						)

	# 					],
	# 					"layout":go.Layout(
	# 						title='scatter plot',
	# 						xaxis={'title':'Date'},
	# 						yaxis={'title':'Closing Rate'}
	# 					)
	# 				}

	# 			)				
	# 		])        		


    #     ]),
    #     dcc.Tab(label='ADA-USD Crypto Data',children=[
	# 		html.Div([
	# 			html.H2("Actual closing price",style={"textAlign": "center"}),
    #             html.H3(f"Price prediction for tomorrow: {lastest_ada[0][0]:.2f} USD",style={"textAlign": "center"}),
	# 			dcc.Graph(
	# 				id="Actual Data ADA",
	# 				figure={
	# 					"data":[
	# 						go.Scatter(
	# 							x=rp_ada.index,
	# 							y=rp_ada["Close"],
	# 							mode='markers'
	# 						)

	# 					],
	# 					"layout":go.Layout(
	# 						title='scatter plot',
	# 						xaxis={'title':'Date'},
	# 						yaxis={'title':'Closing Rate'}
	# 					)
	# 				}

	# 			),
	# 			html.H2("LSTM Predicted closing price",style={"textAlign": "center"}),
	# 			dcc.Graph(
	# 				id="Predicted Data ADA",
	# 				figure={
	# 					"data":[
	# 						go.Scatter(
	# 							x=valid_ada.index,
	# 							y=valid_ada["Predictions"],
	# 							mode='markers'
	# 						)

	# 					],
	# 					"layout":go.Layout(
	# 						title='scatter plot',
	# 						xaxis={'title':'Date'},
	# 						yaxis={'title':'Closing Rate'}
	# 					)
	# 				}

	# 			)				
	# 		])        		


    #     ])

    ])
])


if __name__=='__main__':
	app.run_server(debug=True)