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


class TestPostRequests(unittest.TestCase):

    def test_post_sensor(self):
        for sensor in sensors:
            putResponse = requests.put(
                BASE + f"sensor/sensor_id={sensor['sensor_id']}/city={sensor['city']}/country={sensor['country']}")
            self.assertEqual(putResponse.status_code, 200)
            self.assertEqual(len(putResponse.json()), 2)

    def test_post_weather_data(self):
        for entry in weatherDataEntries:
            putResponse = requests.put(BASE + "/data/sensor=1234", entry)
            self.assertEqual(putResponse.status_code, 201)
            self.assertEqual(len(putResponse.json()), 6)


class TestGetRequests(unittest.TestCase):

    def test_get_sensor(self):
        for sensor in sensors:
            getResponse = requests.get(
                BASE + f"sensor/sensor_id={sensor['sensor_id']}/city={sensor['city']}/country={sensor['country']}")
            self.assertEqual(getResponse.status_code, 200)
            self.assertEqual(len(getResponse.json()), 3)

    

if __name__ == "__main__":
    unittest.main()
