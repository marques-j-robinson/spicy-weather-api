from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import python_weather


app = Flask(__name__)
app.debug = True
CORS(app)


locations = ["new-york", "seattle", "san-antonio"]


def getSpice(temp):
    # super windy == "blow me"
    # smoggy == "the air is poison"
    if temp <= 32:
        return 'Hell hath frozen over'
    elif temp > 32 and temp <= 75:
        return "I'd build a summer home here"
    elif temp > 75:
        return "It's hot as balls"


async def getweather(location):
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(location)
        temp = weather.current.temperature
        res = {
            'location': location,
            'current': {
                'temp': temp,
                'description': weather.current.description,
                'spice': getSpice(temp),
            },
            'forecasts': [],
        }
        for forecast in weather.forecasts:
            day = {
                'date': forecast.date,
                'moon-phase': str(forecast.astronomy.moon_phase),
                'sun-rise': str(forecast.astronomy.sun_rise),
                'sun-set': str(forecast.astronomy.sun_set),
                'temp': forecast.temperature,
                'hourly': [],
            }
            for hourly in forecast.hourly:
                hour = {
                    'time': hourly.time,
                    'temp': hourly.temperature,
                    'description': hourly.description,
                }
                day['hourly'].append(hour)
            res['forecasts'].append(day)
        return res


@app.route('/')
def index():
    return 'Welcome to the Spicy Weather API'


@app.route('/locations')
def get_locations():
    return jsonify(data=locations)


@app.route('/weather/<location>')
async def weather(location):
    return jsonify(data=await getweather(location))


if __name__ == "__main__":
    app.run(host='0.0.0.0')