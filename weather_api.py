from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

import datetime

#  Create app and api
app = Flask(__name__)
api = Api(app)

# Create app to db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/weatherData.db'

# Create a db for the app
db = SQLAlchemy(app)

# create the scheme for the Sensor data
# Using sensor_id as pk and linking to the weatherEntryModel
class SensorModel(db.Model):
    __tablename__ = 'sensortable'
    sensor_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    country = db.Column(db.String(120), unique=True, nullable=False)

    weather_entry = db.relationship('WeatherEntryModel', backref='sensortable')

# Create the scheme for a weather data entry 
# setting a auto increment int as pk
class WeatherEntryModel(db.Model):
    __tablename__ = 'weatherentry'
    weatherentry_id = db.Column(db.Integer, db.Sequence(
        'seq_reg_id', start=1, increment=1), primary_key=True)
    sensor = db.Column(db.Integer, db.ForeignKey('sensortable.sensor_id'))
    # The datetime is automatically created when the data entry is made
    created_at = db.Column(
        db.DateTime, default=datetime.datetime.now(), nullable=False)
    temp = db.Column(db.Integer, nullable=False)
    pop = db.Column(db.Integer, nullable=False)
    humidity = db.Column(db.Integer, nullable=False)
    wind_speed = db.Column(db.Integer, nullable=False)

# This creates the database but only needs to run once and while the local server is running it can mess with requests if left on
# x=1
# while x < 2:
#   db.create_all()
#   x = x+1

# Define values returned in sensor put request
sensor_resource_fields = {
  "city": fields.String,
  "country": fields.String,
}

# Define values returned in sensor get request
sensor_get_resource_fields = {
  "sensor_id": fields.Integer,
  "city": fields.String,
  "country": fields.String}

# Resource to handle queries about the sensor
class Sensor(Resource):
    # Adds a sensor (if the id is unique) to the db
    @marshal_with(sensor_resource_fields)
    def put(self, sensor_id, city, country):
        # Grab the first result if the id exists and abort
        result = SensorModel.query.filter_by(sensor_id=sensor_id).first()
        if result:
            abort(409, message="Sensor id is taken...")
        # if not then create the sensor with the SensorModel
        sensor = SensorModel(sensor_id=sensor_id, city=city, country=country)
        # temperally add the sensor to the database
        db.session.add(sensor)
        # commit changes to db
        db.session.commit()
        # return sensor and code 200
        return sensor, 200

    # Get sensor info from db
    @marshal_with(sensor_get_resource_fields)
    def get(self, sensor_id, city, country):
        # Grab the first result and if there is none abort
        result = SensorModel.query.filter_by(sensor_id=sensor_id).first()
        if not result:
            abort(404, message="Could not find sensor with that id...")
        
        return result

# Define values needed in weather data put and get request 
weather_data_resource_fields = {
  "sensor": fields.Integer,
  "temp": fields.Integer,
  "pop": fields.Integer,
  "humidity": fields.Integer,
  "wind_speed": fields.Integer,
  "created_at": fields.DateTime
}

# Create a new RequestParser object
# this will automatically parse through the request being sent
# and make sure it fits the guidelines provided below that and has the correct information in it
data_add_args = reqparse.RequestParser()

# Add the arguments that are required to make a data entry
data_add_args.add_argument("temp", type=int, help="Enter temperature in Celsius", required=True)
data_add_args.add_argument("pop", type=int, help="Enter probability of precipitation in integer (e.g. for 20% input 20)", required=True)
data_add_args.add_argument("humidity", type=int, help="Enter humidity in hygrometers", required=True)
data_add_args.add_argument("wind_speed", type=int, help="Enter wind speed in km/hr", required=True)

# Resource to handle queries about the sensor
class WeatherEntry(Resource):
    @marshal_with(weather_data_resource_fields)
    def put(self, sensor_id):
      args = data_add_args.parse_args()
      # Create a new data entry from the WeatherEntryModel and attach it to a sensor
      data = WeatherEntryModel(sensor=sensor_id, temp=args["temp"], pop=args["pop"], humidity=args["humidity"], wind_speed=args["wind_speed"])
      db.session.add(data)
      db.session.commit()
      return data, 201

    @marshal_with(weather_data_resource_fields)
    def get(self, sensor_id):
    
        result = WeatherEntryModel.query.filter_by(sensor=sensor_id).all()
        if not result:
            abort(404, message="Could not find sensor with that id...")
        
        return result, 200
    
    
class AveragesOfWeatherData(Resource):
    
    def get(self, sensor_ids, days, metrics):
        # Get the date relevant to the number of days entered in datetime format.
        date = datetime.datetime.now() - datetime.timedelta(days)        

        # This is the final dictionary returned
        sensors_avg_metrics = {}
        # grab all metrics and sensors
        metrics_array = metrics.split(';')
        sensors_array = sensor_ids.split(';')
        metric_values = {}
        # For each sensor the user requests get all the weather data for that one (I would start with date I think and then use sensor to narrow down further)
        for sensor in sensors_array:
          results = WeatherEntryModel.query.filter_by(sensor=sensor).all()
          metric_values_list = []
          # for each metric the user has chosen make a list of all the values in one array and get the average
          for metric in metrics_array:
            for result in results:
              # Get all data entries in the date range:
              if result.created_at >= date:
                metric_values_list.append(getattr(result, metric))
            if len(metric_values_list) > 0:
              metric_values["avg_" + metric] = sum(metric_values_list) / len(metric_values_list)
          # add them all to the dict to be returned with the sensor as their key
          sensors_avg_metrics[sensor] = metric_values
      
        return sensors_avg_metrics, 200

# Create the urls to make requests to the api
api.add_resource(
    Sensor, "/sensor/sensor_id=<int:sensor_id>/city=<string:city>/country=<string:country>")

api.add_resource(WeatherEntry, "/data/sensor=<string:sensor_id>")

api.add_resource(AveragesOfWeatherData, "/avg_data/sensor=<string:sensor_ids>/days=<int:days>/metrics=<string:metrics>")

# Start server
if __name__ == "__main__":
    # Start application in debug mode (not to be used production env)
    app.run(debug=True)
