from flask import Flask, render_template, request, jsonify
import folium
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    start_coords = (54.2361, -4.5481)
    folium_map = folium.Map(location=start_coords, zoom_start=6)

    if request.method == 'POST':
        input_value = request.form['input']
        if "," in input_value:  # Assume input is Easting,Northing
            easting, northing = map(float, input_value.split(','))
            # Convert Easting and Northing to latitude and longitude
            response = requests.get(f'http://api.postcodes.io/postcodes?lon={easting}&lat={northing}')
        else:
            response = requests.get(f'http://api.postcodes.io/postcodes/{input_value}')

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 200 and data['result']:
                lat = data['result'][0]['latitude']
                lon = data['result'][0]['longitude']
                folium_map = folium.Map(location=[lat, lon], zoom_start=17)
                folium.Marker([lat, lon], tooltip='Click for more', popup=input_value).add_to(folium_map)
            else:
                return render_template('map.html', folium_map=folium_map._repr_html_(), error="No results found.")
        else:
            return render_template('map.html', folium_map=folium_map._repr_html_(), error="Failed to fetch data.")

    folium_map = folium_map._repr_html_()
    return render_template('map.html', folium_map=folium_map, error=None)

if __name__ == '__main__':
    app.run(debug=True)