from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import Note
from . import db_1
import json
import requests
import yfinance as yf
import json
import plotly
import plotly.graph_objs as go
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, accuracy_score
from sklearn.model_selection import train_test_split
import pickle
import pymongo
from flask_pymongo import PyMongo
import email, smtplib, ssl
import multiprocessing
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

# from bs4 import BeautifulSoup
# import requests

views = Blueprint('views', __name__)

crypto_data = None 
@views.route('/', methods=['GET'])
@login_required
def home():
    global crypto_data
    if crypto_data is None: # If crypto_data is not yet defined, make the API request
        key='073491ce-1b96-4598-b4c7-43b722119622'
        crypto_data = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&cryptocurrency_type=tokens&convert=BTC', headers={'X-CMC_PRO_API_KEY': '073491ce-1b96-4598-b4c7-43b722119622'}) # Replace YOUR_API_KEY with the key in your account
        crypto_data = crypto_data.json()
        print(crypto_data)
    return render_template("home.html", user=current_user,crypto_data=crypto_data)

@views.route('/set_reminders', methods=['GET','POST'])
@login_required
def set_reminders():

    if(request.method == 'POST'):
        name=request.form['crypto'] 
        price=request.form['price'] 
        name=mapping(name)
        proc1 = multiprocessing.Process(target=send_reminder, args=(name,float(price)))
        proc1.start()
        flash('Reminder set successfully!', category='success')

    return render_template("setreminders.html",user=current_user)


@views.route('/view_graph', methods=['GET', 'POST'])
@login_required
def view_graph():    
    if request.method == 'POST':
        crypto_name = request.form['crypto'] 
        crypto_ticker=mapping(crypto_name)   
        today= date.today()
        last_year= today-relativedelta(years=1)
        crypto_data = yf.download(crypto_ticker, start=last_year, end=today)
        traces = go.Scatter(x=crypto_data.index, y=crypto_data['Close'], name=crypto_ticker) 
        layout = go.Layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label='1d', step='day', stepmode='backward'),
                        dict(count=7, label='1w', step='day', stepmode='backward'),
                        dict(count=1, label='1m', step='month', stepmode='backward'),
                        dict(count=6, label='6m', step='month', stepmode='backward'),
                        dict(step='all')
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type='date',
                title='Date'
            ),
            yaxis=dict(
                title='Price (USD)'
            ),
            title='Crypto Prices'
        )
        fig = go.Figure(data=traces, layout=layout)
        fig.show()
        
    return render_template("graph.html")

@views.route('/predict_price', methods=['GET','POST'])
@login_required
def predict_price():
    x=""
    if request.method == 'POST':
        crypto_name = request.form['crypto']
        print(crypto_name)
        crypto_ticker=mapping(crypto_name)   
        # for crypto_name, crypto_ticker in crypto.items():
        crypto_data = yf.download(crypto_ticker, period='max')
        crypto_data['Prediction'] = crypto_data['Close'].shift(-1)
        last_day = np.array(crypto_data.drop(['Prediction'], axis=1))[-1]
        con=db_1['model']
        print()
        data=con.find({'name':crypto_ticker})
        print(data)
        d={}
        for i in data:
            d=i
        pickled_model=d['lr']
        lr_model=pickle.loads(pickled_model)
        x = lr_model.predict([last_day])[0]
        print(x)
        # print(f"{crypto_name} Next Day Prediction:", next_day_prediction,"USD")
        # output = execute('./script')
        return render_template("predictprice.html", y="Predicted value of "+crypto_name+" for tomorrow is "+str(x))

    return render_template("predictprice.html", y=x)

def send_reminder(name,price):
    print("executing",name)
    crypto_data=yf.download(tickers=name,period='1d',interval = '1m')
    p=np.array(crypto_data['Close'])[-1]
    print(p)
    if(p<price):
        while(True):
            crypto_data=yf.download(tickers=name,period='1d',interval = '1m')
            p=np.array(crypto_data['Close'])[-1]
            if(p>=price):
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                subject = "Crypto market Alert!!!"
                body = "This is to remind you that the "+name+"has crossed "+price+" at "+current_time
                sender_email = "19bd1a051e@gmail.com"
                receiver_email = current_user.email
                password = "Pathuri@123"
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message["Bcc"] = receiver_email  
                message.attach(MIMEText(body, "plain"))
                text = message.as_string()
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)
                break
    else:
        while(True):
            crypto_data=yf.download(tickers=name,period='1d',interval = '1m')
            p=np.array(crypto_data['Close'])[-1]
            if(p<=price):
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                subject = "Crypto market Alert!!!"
                body = "This is to remind you that the "+name+"has dropped to "+price+" at "+current_time
                sender_email = "19bd1a051e@gmail.com"
                receiver_email = current_user.email
                password = "Pathuri@123"
                message = MIMEMultipart()
                message["From"] = sender_email
                message["To"] = receiver_email
                message["Subject"] = subject
                message["Bcc"] = receiver_email  
                message.attach(MIMEText(body, "plain"))
                text = message.as_string()
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, text)
                break
def mapping(crypto_name):
    if crypto_name== 'Bitcoin':
        crypto_ticker='BTC-USD'
    elif crypto_name== 'Ethereum':
        crypto_ticker='ETH-USD'
    elif crypto_name== 'Tether ':
        crypto_ticker='USDT-USD'
    elif crypto_name== 'BNB':
        crypto_ticker='BNB-USD'
    elif crypto_name== 'USD Coin':
        crypto_ticker='USDC-USD'
    elif crypto_name== 'XRP':
        crypto_ticker='XRP'
    elif crypto_name== 'Cardano':
        crypto_ticker='ADA-USD'
    elif crypto_name== 'Polygon':
        crypto_ticker='MATIC-USD'
    elif crypto_name== 'Dogecoin':
        crypto_ticker='DOGE-USD'
    elif crypto_name== 'Binance USD':
        crypto_ticker='BUSD-USD'
    elif crypto_name== 'Solana':
        crypto_ticker='SOL-USD'
    elif crypto_name== 'Polkadot':
        crypto_ticker='DOT-USD'
    return crypto_ticker