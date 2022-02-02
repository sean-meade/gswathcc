import unittest
from weather_api import app
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



class TestSensorRequests(unittest.TestCase):

  def test_post_sensor(self):
    for sensor in sensors:
      putResponse = requests.put(BASE + f"sensor/sensor_id={sensor['sensor_id']}/city={sensor['city']}/country={sensor['country']}")
      self.assertEqual(putResponse.status_code, 200)
      self.assertEqual(len(putResponse.json()), 2)


if __name__ == "__main__":
  unittest.main()