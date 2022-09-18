from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import python_weather


app = Flask(__name__)
app.debug = True
CORS(app)


locations = ["new-york", "seattle", "san-antonio"]


def getSpice(temp):
    if temp <= 32:
        return 'Hell hath frozen over'
    elif temp > 0 and temp <= 75:
        return "I'd build a summer home here"
    elif temp > 75:
        return "It's hot as balls"


async def getweather(city):
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(city)
        temp = weather.current.temperature
        res = {
            'temp': temp,
            'description': weather.current.description,
            'spice': getSpice(temp),
        }
        return res


@app.route('/')
def index():
    return 'Welcome to the Spicy Weather API'


@app.route('/locations')
def get_locations():
    return jsonify(data=list(all_locations.keys()))


@app.route('/weather/<city>')
async def weather(city):
    return jsonify(data=await getweather(city))


if __name__ == "__main__":
    app.run(host='0.0.0.0')