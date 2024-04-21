from flask import Flask, render_template, request
import folium
import requests
from pyproj import Proj, transform

app = Flask(__name__)

# Convert Eastings and Northings to Lat/Lon
def convert_en_to_latlon(easting, northing):
    in_proj = Proj('epsg:27700')  # OSGB36
    out_proj = Proj('epsg:4326')  # WGS84
    lon, lat = transform(in_proj, out_proj, easting, northing)
    return [lat, lon]

@app.route('/', methods=['GET', 'POST'])
def map_view():
    # Create a Folium map
    uk_map = folium.Map(location=[54.5, -4], zoom_start=6)

    if request.method == 'POST':
        search_query = request.form['search_query']
        search_type = request.form['search_type']

        if search_type == 'postcode':
            location = get_location_by_postcode(search_query)
        elif search_type == 'place_name':
            location = get_location_by_place_name(search_query, 'YOUR_API_KEY_HERE')
        elif search_type == 'coordinates':
            easting, northing = map(int, search_query.split(','))
            location = convert_en_to_latlon(easting, northing)
        
        if location:
            folium.Marker(location, popup='Location Found').add_to(uk_map)

    # Save the map as HTML
    map_html = uk_map._repr_html_()

    # Render the HTML with the form and the map
    return render_template('map.html', map_html=map_html)

if __name__ == '__main__':
    app.run(debug=True)