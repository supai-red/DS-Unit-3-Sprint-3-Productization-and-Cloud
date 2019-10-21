"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq
import requests

APP = Flask(__name__)

APP.config ['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
DB = SQLAlchemy(APP)

SQLALCHEMY_TRACK_MODIFICATIONS = False
API = openaq.OpenAQ()

@APP.route('/')
def root():
    """Retrieving API data"""
    request = API.measurements(city='Los Angeles', parameter='pm25')
    """Creating list of tuples with datetime/utc values"""
    status, resp = request
    resp.keys()
    date = []
    for i in (resp['results']):
        date.append(i['date'])
    ld = [d.get('local', None) for d in date]  # create list 1
    ld2 = [d2.get('utc', None) for d2 in date] #create list 2
    merged_list = tuple(zip(ld, ld2))
    return str(Record.query.filter(Record.value >=10).all)
           # str(merged_list) - original return to produce page of tuples

"""Class Record as given"""
class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    # TODO Get data from OpenAQ, make Record objects with it, and add to # Db
    """Building list of values"""
    value_list = []
    for i in (resp['results']):
        value_list.append(i['value'])
    """Creating records for db"""
    for i in range(len(merged_list)):
        id = i
        datetime = str(merged_list[i])
        value = int(value_list[i])
        rec = Record(id=id, datetime=datetime, value=value)
        DB.session.add(rec)
    DB.session.commit()
    return 'Data refreshed!'

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return 'TODO - write a nice representation of Records'

if __name__ == '__main__':
     main()
