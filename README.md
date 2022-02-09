To run the API in weather_api.py you will need the packages listed in requirements.txt  

To start running the weather API locally run the  the weather_api.py with the following command in the terminal:

`python weather_api.py`

In a separate terminal you can run the test_weather_api.py to test certain portions of the code (currently failing for test_get_sensor):

`python test_weather_api.py`

This will also have loaded data into the sqlalchemy database.

To test if the data successfully stored use the following as a url in your browser: `http://127.0.0.1:5000/data/sensor=1234`

If you see the following it means that there are both sensors and weather data (connected to those sensors):

[
    {
        "sensor": 1234,
        "temp": 10,
        "pop": 20,
        "humidity": 30,
        "wind_speed": 40,
        "created_at": "Wed, 02 Feb 2022 23:32:49 -0000"
    },
    {
        "sensor": 1234,
        "temp": 1,
        "pop": 2,
        "humidity": 3,
        "wind_speed": 4,
        "created_at": "Wed, 02 Feb 2022 23:32:49 -0000"
    },
    {
        "sensor": 1234,
        "temp": 2,
        "pop": 4,
        "humidity": 6,
        "wind_speed": 8,
        "created_at": "Wed, 02 Feb 2022 23:32:49 -0000"
    }
]

In test.py you can define your own values and add entries into the database that way as well.

Finally you can request the average of all the data for sensor(s) by creating the following url (the example below should work if test_weather_api.py has been run):

e.g: http://127.0.0.1:5000/avg_data/sensor=1234;4321;5678;8765/days=5/metrics=temp;humidity;pop;wind_speed

<p>http://127.0.0.1:5000/avg_data/sensor=<b>sensor_ids</b>/days=<b>days</b>/metrics=<b>metrics</b></p>

where:
sensor_ids: is a string of sensor ids separated by a semi colon (;)
days: is an integer representing the number of days of weather data you want from the current day
metrics: sensor_ids: is a string of metrics separated by a semi colon (;)

Notes:
if test_weather_api.py is running you can use some pre defined sensor_ids (1234, 4321, 5678, 8765) and any you have created.

days currently doesn't do anything but check AveragesOfWeatherData for an explanation of what my plan was

metrics are temp, humidity, pop, and wind_speed

