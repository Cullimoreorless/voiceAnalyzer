from datetime import datetime

from voiceAnalyzer import db
from sqlalchemy import desc

class TwitterSubmittedUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    submitteddate = db.Column(db.DateTime, default = datetime.utcnow())
    submitterdata = db.Column(db.String(100))

    def __repr__(self):
        return '<TwitterSubmittedUser {}: {}'.format(self.id, self.username)

