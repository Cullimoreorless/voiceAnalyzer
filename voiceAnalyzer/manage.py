#! /usr/bin/env python

from voiceAnalyzer import app, db
from flask_script import Manager, prompt_bool



manager = Manager(app)

@manager.command
def initdb():
    db.create_all()
    db.session.commit()
    print('initialized the database')

@manager.command
def dropdb():
    if prompt_bool(  "Are you sure you want to drop the database?"):
        db.drop_all()
        print('dropped it, you fool')

if __name__ == '__main__':
    manager.run()