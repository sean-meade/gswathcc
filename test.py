import requests

BASE = "http://127.0.0.1:5000/"

putResponse = requests.put(BASE + "sensor/sensor_id=30/city=clare/country=ireland")
print(putResponse.json())


getResponse = requests.get(BASE + "sensor/sensor_id=30/city=d/country=trk")
print(getResponse.json())