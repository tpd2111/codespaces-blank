# app.py
from flask import Flask, request, jsonify, render_template
import folium
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    search_type = request.form.get('type')
    query = request.form.get('query')

    if search_type == 'postcode':
        return search_postcode(query)
    elif search_type == 'coordinates':
        easting, northing = map(float, query.split(','))
        return search_coordinates(easting, northing)
    elif search_type == 'placename':
        return search_placename(query)
    else:
        return jsonify({'error': 'Invalid search type'})

def search_postcode(postcode):
    url = f'http://api.postcodes.io/postcodes/{postcode}'
    response = requests.get(url)
    data = response.json()
    if data['status'] == 200:
        lat, lon = data['result']['latitude'], data['result']['longitude']
        return jsonify({'latitude': lat, 'longitude': lon})
    else:
        return jsonify({'error': 'Postcode not found'})

def search_coordinates(easting, northing):
    # Here you would normally convert Easting/Northing to Latitude/Longitude
    latitude, longitude = easting / 100000, northing / 100000  # Simplified
    return jsonify({'latitude': latitude, 'longitude': longitude})

def search_placename(name):
    api_key = 'YOUR_API_KEY'
    url = f'https://api.os.uk/search/places/v1/find?query={name}&key={api_key}'
    response = requests.get(url)
    data = response.json()
    if 'results' in data:
        lat, lon = data['results'][0]['LATITUDE'], data['results'][0]['LONGITUDE']
        return jsonify({'latitude': lat, 'longitude': lon})
    else:
        return jsonify({'error': 'Place not found'})

if __name__ == '__main__':
    app.run(debug=True)