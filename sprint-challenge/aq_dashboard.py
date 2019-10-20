"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests



"""Setting an instance of the Flask App"""
APP = Flask(__name__)
APP.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
API = openaq.OpenAQ()
    # Pointing to the location database will populate.

@APP.route('/')
def root():
    """Base view."""
    return str(Record.query.filter(Record.value >=10).all)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    request = api.measurements(city='Los Angeles', parameter='pm25')
    status, resp = request
    date = []
    for i in resp['results']:
        date.append(i['date'])
        DB.session.add(Record(datetime=date))
    DB.session.commit()
    return 'Data refreshed!'

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<Record: {} >'.format(self.datetime, self.value)

if __name__ == '__main__':
    root()
