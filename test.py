import requests

BASE = "http://127.0.0.1:5000/"

# Requests for Sensors 

# define your own sensor_id, city and country to add it to the sensor table in the database
putResponse = requests.put(BASE + "sensor/sensor_id=30/city=clare/country=ireland")
print(putResponse.json())

# You need to give all 3 to request information for a sensor but the sensor_id is the only thing that has to be correct
getResponse = requests.get(BASE + "sensor/sensor_id=30/city=d/country=trk")
print(getResponse.status_code)

# Requests for data

# Sensors to run tests
sensors = [{
    "sensor_id": 2222,
    "city": "Cork",
    "country": "Ireland"},
    {
    "sensor_id": 4444,
    "city": "Ealing",
    "country": "England"},
    {
    "sensor_id": 7777,
    "city": "Edinburgh",
    "country": "Scotland"},
    {
    "sensor_id": 9999,
    "city": "Swansea",
    "country": "Wales"}
]

# you can add the above sensors to the database or create more in the list
def pre_fill_values(sensors):
  for sensor in sensors:
      requests.put(
          BASE + f"sensor/sensor_id={sensor['sensor_id']}/city={sensor['city']}/country={sensor['country']}")

pre_fill_values(sensors)

weatherDataEntries = [{
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
}, {
    "temp": 2,
    "pop": 4,
    "humidity": 6,
    "wind_speed": 8,
}]

# You can enter a specific data entry from above by supplyin the sensor id in sensor and choosing which element in the list weatherDataEntries
putResponse = requests.put(BASE + "/data/sensor=1234", weatherDataEntries[0])
print(putResponse.status_code)

# AveragesOfWeatherData request

# get the average metrics of a sensor by changing the value of sensor and adding or taking (or both) in metrics
getResponse = requests.get(BASE + "/avg_data/sensor=1234/days=3/metrics=temp;humidity")
print(getResponse.json())