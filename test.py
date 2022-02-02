import requests

from weather_api import WeatherEntry

BASE = "http://127.0.0.1:5000/"

# Requests for Sensors 

# putResponse = requests.put(BASE + "sensor/sensor_id=30/city=clare/country=ireland")
# print(putResponse.json())

# getResponse = requests.get(BASE + "sensor/sensor_id=30/city=d/country=trk")
# print(getResponse.json())

# Requests for data

weatherEntries = [{
  "temp": 10,
  "pop": 20,
  "humidity": 30,
  "wind_speed": 40,
  },
  {
  "temp": 1,
  "pop": 2,
  "humidity": 3,
  "wind_speed": 4,
  },{
  "temp": 2,
  "pop": 4,
  "humidity": 6,
  "wind_speed": 8,
  }]

# putResponse = requests.put(BASE + "/data/sensor=1234", weatherEntries[0])
# print(putResponse.json())

# getResponse = requests.get(BASE + "/data/sensor=1234")
# print(getResponse.json())

# AveragesOfWeatherData request

getResponse = requests.get(BASE + "/avg_data/sensor=1234/days=3/metrics=temp;humidity")
print(getResponse.json())