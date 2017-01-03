from flask import render_template, flash, redirect, url_for

from voiceAnalyzer import app, db
from voiceAnalyzer.forms import TwitterUserForm

@app.route('/')
@app.route('/voice/twitter')
def home():
    form = TwitterUserForm();
    return render_template('base.html', form=form)
    
@app.route('/voice/twitter/analyze', methods=['GET','POST'])
def analyzeUser(user):
    

# TODO Steps
#     - set up python twitter api
#     - use some R wrapper to create most used words plot
#     - figure out how to surface json data, test
#         on the retrieval server and client side,
#     - deploy to alexcullimore.com
