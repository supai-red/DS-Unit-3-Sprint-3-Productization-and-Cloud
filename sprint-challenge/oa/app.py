"""OpenAQ Air Quality Dashboard with Flask."""
from decouple import config
from flask import Flask, render_template, request
import requests
import openaq
from .models import DB, Record

def create_app():
    """create and configure instance of Flask app"""
    app = Flask(__name__)

    # Pointing to the location database will populate.
    app.config['SQLALCHEMY_DATABASE_URI'] = ""sqlite:///C:\\Users\\Andrea\\Desktop\\MyRepo\\C:\Users\Andrea\Desktop\MyRepo\DS-Unit-3-Sprint-3-Productization-and-ClouC:\Users\Andrea\Desktop\MyRepo\DS-Unit-3-Sprint-3-Productization-and-Cloud\\sprint-challenge\\db.sqlite3""

    DB.init_app(app)

    @app.route('/')
    def root():
        """Base view."""
        return render_template('home.html')

    @app.route('/data/')
    def connect():
        "Establishing connection to API"
        api = openaq.OpenAQ()
        x = api.measurements(city='Los Angeles', parameter='pm25')
        status, resp = x
        datetime_list = []
        for i in resp['results']:
            datetime.append(i['date'])
            dl = [d.get('local', None) for d in date]

        for i in dl:
            rec = Record(datetime=i)
            DB.session.add(rec)
        DB.session.commit()
        return render_template('home.html')

    @app.route('/refresh')
    def refresh():
        """Pull fresh data from Open AQ and replace existing data."""
        DB.drop_all()
        DB.create_all()
        # TODO Get data from OpenAQ, make Record objects with it, and add to db
        DB.session.commit()
        return 'Data refreshed!'

    return app
