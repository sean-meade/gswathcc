from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import datetime


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'

db = SQLAlchemy(app)

class SensorModel(db.Model):
  __tablename__ = 'sensortable'
  sensor_id = db.Column(db.Integer, primary_key=True)
  city = db.Column(db.String(80), unique=True, nullable=False)
  country = db.Column(db.String(120), unique=True, nullable=False)

  weather_entry = db.relationship('WeatherEntryModel', backref='sensortable')

class WeatherEntryModel(db.Model):
  __tablename__ = 'weatherentry'
  weatherentry_id = db.Column(db.Integer, db.Sequence('seq_reg_id', start=1, increment=1), primary_key=True)
  sensor = db.Column(db.Integer, db.ForeignKey('sensortable.sensor_id'))
  created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=False, )
  temp = db.Column(db.Integer, nullable=False)
  pop = db.Column(db.Integer, nullable=False)
  humidity = db.Column(db.Integer, nullable=False)
  wind_speed = db.Column(db.Integer, nullable=False)