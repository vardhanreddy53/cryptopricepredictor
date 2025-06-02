from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
import json
import requests
import yfinance as yf
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
from bs4 import BeautifulSoup
import requests
import pickle
import pymongo




# x=""
# crypto_ticker=input("enter coin: ")
# crypto_data = yf.download(crypto_ticker, period='max')
# crypto_data['Prediction'] = crypto_data['Close'].shift(-1)
# X = np.array(crypto_data.drop(['Prediction'], 1))
# X = X[:-1]
# y = np.array(crypto_data['Prediction'])
# y = y[:-1]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
# lr_model = LinearRegression()
# lr_model.fit(X_train, y_train)
# predictions = lr_model.predict(X_test)
# # accuracy = accuracy_score(y_test, predictions)
# mse = mean_squared_error(y_test, predictions)
# print(f"{crypto_ticker} Mean Squared Error:", mse)
# # print(f"{crypto_ticker} Accuracy:", accuracy)
# last_day = np.array(crypto_data.drop(['Prediction'], 1))[-1]
# x = lr_model.predict([last_day])[0]
# print(x)
# model=pickle.dumps(lr_model)
# myclient=pymongo.MongoClient('mongodb://localhost:27017/')
# db=myclient['major_project']
# con=db['model']
# info=con.insert_one({'lr':model,'name':'lr'})
# print('done')





# import numpy as np
# import pandas as pd
# import pandas_datareader as web
# from sklearn.preprocessing import MinMaxScaler
# from keras.models import Sequential
# from keras.layers import Dense, LSTM

# # Load the data from Yahoo Finance
# symbol = 'BTC-USD' # Replace with your desired cryptocurrency symbol
# df = web.DataReader(symbol, data_source='yahoo', start='2018-01-01', end='2024-03-31')

# # Normalize the data
# scaler = MinMaxScaler(feature_range=(0, 1))
# df['Close'] = scaler.fit_transform(np.array(df['Close']).reshape(-1, 1))

# # Split the data into train and test sets
# training_size = int(len(df) * 0.8)
# train_data = df[0:training_size]
# test_data = df[training_size:]

# # Prepare the data for LSTM
# def create_dataset(dataset, look_back=1):
#     data_X, data_Y = [], []
#     for i in range(len(dataset) - look_back - 1):
#         a = dataset[i:(i+look_back), 0]
#         data_X.append(a)
#         data_Y.append(dataset[i + look_back, 0])
#     return np.array(data_X), np.array(data_Y)

# look_back = 30
# train_X, train_Y = create_dataset(train_data.values, look_back)
# test_X, test_Y = create_dataset(test_data.values, look_back)

# # Reshape the data for LSTM
# train_X = np.reshape(train_X, (train_X.shape[0], 1, train_X.shape[1]))
# test_X = np.reshape(test_X, (test_X.shape[0], 1, test_X.shape[1]))

# # Build the LSTM model
# model = Sequential()
# model.add(LSTM(units=50, return_sequences=True, input_shape=(1, look_back)))
# model.add(LSTM(units=50))
# model.add(Dense(1))

# # Compile the model
# model.compile(loss='mean_squared_error', optimizer='adam')

# # Train the model
# model.fit(train_X, train_Y, epochs=100, batch_size=32)

# # Make predictions
# train_predict = model.predict(train_X)
# test_predict = model.predict(test_X)

# # Invert the predictions
# train_predict = scaler.inverse_transform(train_predict)
# train_Y = scaler.inverse_transform([train_Y])
# test_predict = scaler.inverse_transform(test_predict)
# test_Y = scaler.inverse_transform([test_Y])

# # Calculate the root mean squared error
# train_rmse = np.sqrt(np.mean(np.power(train_Y - train_predict, 2)))
# test_rmse = np.sqrt(np.mean(np.power(test_Y - test_predict, 2)))
# print("Train RMSE: %f" % train_rmse)
# print("Test RMSE: %f" % test_rmse)











# Import necessary libraries
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestRegressor
# from sklearn.metrics import r2_score

# # Load data from Yahoo Finance
# x=""
# crypto_ticker=input("enter coin: ")
# df = yf.download(crypto_ticker, period='max')
# # df = pd.read_csv('crypto_prices.csv')

# # Define input and output variables
# X = np.array(df.drop(["Close"],1))
# y = df['Close']

# # Split data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Define random forest regression model
# model = RandomForestRegressor(n_estimators=100, random_state=42)

# # Fit model on training data
# model.fit(X_train, y_train)

# # Make predictions on test set
# y_pred = model.predict(X_test)

# # Calculate R^2 score
# r2 = r2_score(y_test, y_pred)
# print('R^2 score:', r2)

# # last_day = np.array(df.drop(['Close'], 1))[-1]
# k = np.array(df.drop(['Close'], 1))[-1]
# x = model.predict([k])[0]
# print(x)
# # Predict price for new data point
# new_data = [[10000, 12000, 9000, 50000000]]
# predicted_price = model.predict(new_data)
# print('Predicted price:', predicted_price)