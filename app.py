from flask import Flask, render_template, request
import folium
import requests

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Set a default location (Center of the UK)
    start_coords = (54.2361, -4.5481)
    # Default zoom level for the initial map
    folium_map = folium.Map(location=start_coords, zoom_start=6)

    if request.method == 'POST':
        postcode = request.form['postcode']
        res = requests.get(f'http://api.postcodes.io/postcodes/{postcode}')
        if res.status_code == 200:
            data = res.json()
            if data['status'] == 200:
                lat = data['result']['latitude']
                lon = data['result']['longitude']
                # Resetting the map center and zoom level specifically after finding the postcode
                folium_map = folium.Map(location=[lat, lon], zoom_start=17)  # Higher zoom level for closer view
                folium.Marker([lat, lon], tooltip='Click for more', popup=postcode).add_to(folium_map)
            else:
                # If the postcode is not found, keep the default map
                folium_map = folium.Map(location=start_coords, zoom_start=6)
        else:
            # If the API call fails, display the default map
            folium_map = folium.Map(location=start_coords, zoom_start=6)

    # Render the map in the HTML template
    folium_map = folium_map._repr_html_()

    return render_template('map.html', folium_map=folium_map)

if __name__ == '__main__':
    app.run(debug=True)