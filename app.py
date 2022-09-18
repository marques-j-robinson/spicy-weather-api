from flask import Flask, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
app.debug = True
CORS(app)


all_locations = {
    'new-york': {
        'temp': -5,
        'spice': 'Hell hath froze over',
    },
    'seattle': {
        'temp': 65,
        'spice': "I'd build a summer home here",
    },
    'san-antonio': {
        'temp': 200,
        'spice': "It's hot as balls",
    },
}


@app.route('/')
def index():
    return 'Welcome to the Spicy Weather API'


@app.route('/locations')
def locations():
    return jsonify(data=list(all_locations.keys()))


@app.route('/weather/<city>')
def weather(city):
    try:
        return jsonify(data=all_locations[city])
    except KeyError:
        return jsonify(data='city_not_found')
    except:
        return jsonify(data='internal_server_error')


if __name__ == "__main__":
    app.run(host='0.0.0.0')