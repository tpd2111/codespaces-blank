from flask import Flask, render_template, request, jsonify
import folium
import requests
import pyproj

app = Flask(__name__)

# Convert Easting and Northing (OSGB36) to Latitude and Longitude (WGS84)
def convert_easting_northing_to_lat_lon(easting, northing):
    osgb36 = pyproj.CRS('EPSG:27700')
    wgs84 = pyproj.CRS('EPSG:4326')
    transformer = pyproj.Transformer.from_crs(osgb36, wgs84, always_xy=True)
    lon, lat = transformer.transform(easting, northing)
    return lat, lon

@app.route('/', methods=['GET', 'POST'])
def index():
    start_coords = (54.2361, -4.5481)
    folium_map = folium.Map(location=start_coords, zoom_start=6)

    if request.method == 'POST':
        input_value = request.form['input']
        try:
            if "," in input_value:  # Assume input is Easting,Northing
                easting, northing = map(int, input_value.split(','))
                lat, lon = convert_easting_northing_to_lat_lon(easting, northing)
            else:  # Assume input is a postcode
                response = requests.get(f'http://api.postcodes.io/postcodes/{input_value}')
                response.raise_for_status()
                data = response.json()
                lat = data['result']['latitude']
                lon = data['result']['longitude']

            # Update the map
            folium_map = folium.Map(location=[lat, lon], zoom_start=17)
            folium.Marker([lat, lon], tooltip='Click for more', popup=input_value).add_to(folium_map)
        except Exception as e:
            return render_template('map.html', folium_map=folium_map._repr_html_(), error=str(e))

    folium_map = folium_map._repr_html_()
    return render_template('map.html', folium_map=folium_map, error=None)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    term = request.args.get('term', '')
    response = requests.get(f'https://api.postcodes.io/postcodes?q={term}&limit=5')
    response.raise_for_status()
    data = response.json()
    suggestions = [{'label': res['postcode'], 'value': res['postcode']} for res in data['result']]
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True)