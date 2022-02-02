import unittest
import weather_api
import requests

BASE = "http://127.0.0.1:5000/"

# Sensors to run tests
sensors = [{
  "sensor_id": 1234,
  "city": "Dublin",
  "country": "Ireland"},
  {
  "sensor_id": 4321,
  "city": "London",
  "country": "England"},
  {
  "sensor_id": 5678,
  "city": "Glasgow",
  "country": "Scotland"},
  {
  "sensor_id": 8765,
  "city": "Cardiff",
  "country": "Wales"}
  ]

print(sensors[0]["sensor_id"])

class TestSensorRequests(unittest.TestCase):

  def test_post_sensor(self):
    for sensor in sensors:

      postResponse = requests.put(BASE + f"/sensor/sensor_id=<int:{sensor['sensor_id']}>/city=<string:{sensor['city']}>/country=<string:{sensor['country']}>")
      self.assertEqual(postResponse.status_code, 200)
      self.assertEqual(len(postResponse.json(), 1))

