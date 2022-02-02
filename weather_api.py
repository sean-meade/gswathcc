from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import datetime

#  Create app and api
app = Flask(__name__)
api = Api(app)

# Create app to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'

# Create a db for the app
db = SQLAlchemy(app)


class SensorModel(db.Model):
    __tablename__ = 'sensortable'
    sensor_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    country = db.Column(db.String(120), unique=True, nullable=False)

    weather_entry = db.relationship('WeatherEntryModel', backref='sensortable')


class WeatherEntryModel(db.Model):
    __tablename__ = 'weatherentry'
    weatherentry_id = db.Column(db.Integer, db.Sequence(
        'seq_reg_id', start=1, increment=1), primary_key=True)
    sensor = db.Column(db.Integer, db.ForeignKey('sensortable.sensor_id'))
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False, )
    temp = db.Column(db.Integer, nullable=False)
    pop = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)

# db.create_all()

sensor_add_args = reqparse.RequestParser()

sensor_add_args.add_argument("city", type=str, help="Enter the City the sensor is in", required=True)
sensor_add_args.add_argument("county", type=str, help="Enter the County the sensor is in", required=True)


sensor_resource_fields = {
  "city": fields.String,
  "country": fields.String,
}

sensor_get_resource_fields = {
  "sensor_id": fields.Integer,
  "city": fields.String,
  "country": fields.String}

# Resource to handle queries about the sensor
class Sensor(Resource):
    @marshal_with(sensor_resource_fields)
    def put(self, sensor_id, city, country):
        result = SensorModel.query.filter_by(sensor_id=sensor_id).first()
        if result:
            abort(409, message="Sensor id is taken...")
        sensor = SensorModel(sensor_id=sensor_id, city=city, country=country)
        # temperally add the video the video to the database
        db.session.add(sensor)
        # commit changes to db (make it permanent)
        db.session.commit()
        return sensor, 200

    @marshal_with(sensor_get_resource_fields)
    def get(self, sensor_id, city, country):
    
        result = SensorModel.query.filter_by(sensor_id=sensor_id).first()
        if not result:
            abort(404, message="Could not find video with that id...")
        # The result is actually an instance of the VideoModel class (it's an object)
        return result


api.add_resource(
    Sensor, "/sensor/sensor_id=<int:sensor_id>/city=<string:city>/country=<string:country>")


# class WeatherEntry(Resource):
#     def put(self, sensor_id):

#         data = WeatherEntryModel(
#             sensor=sensor_id, temp=args["temp"], pop=args["pop"], humidity=args["humidity"], wind_speed=args["wind_speed"])
#         db.session.add(data)
#         db.session.commit()
#         return data, 201

#     def get(self, sensor_ids, metric_felids, days):

#         metrics = metric_felids.split(';')
#         date = datetime.datetime.now() - datetime.timedelta(days)
#         day = date.day
#         month = date.month
#         if sensor_ids == '':
#             result = WeatherEntryModel.query.all()
#         else:
#             sensors = sensor_ids.split(';')

#         for sensor in sensors:
#             result = WeatherEntryModel.query.filter_by(sensor=sensor).all()
#             temps = []
#             humidities = []
#             if result != []:
#                 for r in result:
#                     print(r.temp)
#                     temps.append(r.temp)
#                     humidities.append(r.humidity)
#                 temp_avg = sum(temps) / len(temps)
#                 hum_avg = sum(humidities) / len(humidities)
#                 print(sensor, temp_avg, hum_avg)
#             results = {"sensor": str(sensor), "temp_avg": str(
#                 temp_avg), "hum_avg": str(hum_avg)}

#         # The result is actually an instance of the VideoModel class (it's an object)
#         return results


# Start server
if __name__ == "__main__":
    # Start application in debug mode (not to be used production env)
    app.run(debug=True)
