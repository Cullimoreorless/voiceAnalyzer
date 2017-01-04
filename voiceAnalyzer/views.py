from flask import render_template, flash, redirect, url_for

from voiceAnalyzer import app, db
from voiceAnalyzer.forms import TwitterUserForm
from twitterservice import TwitterService
from pandas import pandas as pd


@app.route('/voice/twitter', methods=['GET','POST'])
def home():
    form = TwitterUserForm();
    dow_data = None
    hod_data = None
    username = None
    sent_data = None
    if form.validate_on_submit():
        username = form.username.data
        ts = TwitterService(username, 1000)
        dow_data = ts.get_tweet_day_of_week_data().to_json(orient='records')
        hod_data = ts.get_tweet_hour_of_day_data().to_json(orient='records')
        sent_data = ts.get_tweet_sentiment_data().to_json(orient='records')
    return render_template(
        'home.html',
        form=form,
        username=username,
        dow_data=dow_data,
        hod_data=hod_data,
        sent_data=sent_data
    )


    
# @app.route('/voice/twitter/analyze', methods=['GET','POST'])
# def analyzeUser(user):
    

# TODO Steps
#     - set up python twitter api
#     - use some R wrapper to create most used words plot
#     - figure out how to surface json data, test
#         on the retrieval server and client side,
#     - deploy to alexcullimore.com
