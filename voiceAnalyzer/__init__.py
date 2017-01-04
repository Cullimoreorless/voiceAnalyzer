import os

from twitter import OAuth, Twitter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from pandas import pandas as pd

sentimentDF = pd.read_csv('./datasets/wordsentiment.csv')

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SECRET_KEY"] = b'v\xb3y\xc4\xb9\x97\x14\xb4\x94\xe83\xee\xb9I\xbe`z>\x9a\x1b%\x98\xad<';
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ os.path.join(basedir, 'twitterAnalyzer.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

consumer_key = "NZC6NuJoqyjnbCxYsyE4BeDlK"
consumer_secret = "79IQqfEIdXUPnule0cHKdpEQQN74ApnkPq1QNHmlzVsOIwo14T"
access_token = "1499062124-3M2uKdsAOw1SX86lcbUkoTa7tK3GQEggSyS8ZT4"
access_secret = "rHYzFHSpP4CLsHycg2GETfTfQ56PwTNFpopGLjAwof3tZ"


oauth = OAuth(access_token, access_secret, consumer_key, consumer_secret)

twitterApi = Twitter(auth=oauth)

import models
import views

