from flask_wtf import Form
from wtforms.fields import StringField
from wtforms.validators import DataRequired

class TwitterUserForm(Form):
    username = StringField('Twitter Handle', validators=[DataRequired()])
    