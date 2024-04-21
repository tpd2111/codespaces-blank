from flask import Flask, render_template, request
import folium
import requests
from pyproj import Proj, transform

app = Flask(__name__)

# Function to convert Eastings and Northings to Lat/Lon
def convert_en_to_latlon(easting, northing):
    # OSGB36 to WGS84
    in_proj = Proj('epsg:27700')
    out_proj = Proj('epsg:4326')
    lon, lat = transform(in_proj, out_proj, easting, northing)
    return [lat, lon]

# Function to get location data from postcode using postcodes.io
def get_location_by_postcode(postcode):
    response = requests.get(f"https://api.postcodes.io/postcodes/{postcode}")
    data = response.json()
    if data['status'] == 200:
        return [data['result']['latitude'], data['result']['longitude']]
    else:
        return None

# Function to get location data from place name using OS Places API
def get_location_by_place_name(place_name, api_key):
    headers = {'Content-Type': 'application/json'}
    params = {
        'key': api_key,
        'query': place_name
    }
    response = requests.get("https://api.os.uk/search/places/v1/find", headers=headers, params=params)
    data = response.json()
    if data['results']:
        return [data['results'][0]['LAT'], data['results'][0]['LON']]
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def map_view():
    uk_map = folium.Map(location=[54.5, -4], zoom_start=6)

    if request.method == 'POST':
        search_type = request.form.get('search_type')
        search_query = request.form.get('search_query')
        api_key = request.form.get('api_key')  # Required for OS Places API

        if search_type == 'postcode':
            location = get_location_by_postcode(search_query)
            if location:
                folium.Marker(location, popup='Postcode Location').add_to(uk_map)
        elif search_type == 'place_name':
            location = get_location_by_place_name(search_query, api_key)
            if location:
                folium.Marker(location, popup='Place Name Location').add_to(uk_map)
        elif search_type == 'coordinates':
            easting, northing = map(int, search_query.split(','))
            location = convert_en_to_latlon(easting, northing)
            folium.Marker(location, popup='Converted E/N to Lat/Lon').add_to(uk_map)

    return uk_map._repr_html_()

if __name__ == '__main__':
    app.run(debug=True)