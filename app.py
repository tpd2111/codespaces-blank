from flask import Flask, render_template, request
import folium
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Set a default location (Center of the UK)
    start_coords = (54.2361, -4.5481)
    folium_map = folium.Map(location=start_coords, zoom_start=4)

    if request.method == 'POST':
        postcode = request.form['postcode']
        res = requests.get(f'http://api.postcodes.io/postcodes/{postcode}')
        if res.status_code == 200:
            data = res.json()
            if data['status'] == 200:
                lat = data['result']['latitude']
                lon = data['result']['longitude']
                folium.Marker([lat, lon], tooltip='Click for more', popup=postcode).add_to(folium_map)
                # Center the map on the searched postcode
                folium_map.location = [lat, lon]
                folium_map.zoom_start = 16

    # Render the map in the HTML template
    folium_map = folium_map._repr_html_()

    return render_template('map.html', folium_map=folium_map)

if __name__ == '__main__':
    app.run(debug=True)