import folium

def create_os_map(api_key, names_api_key, center=(54.5, -4), zoom_start=6):
    # Initialize the map
    m = folium.Map(location=center, zoom_start=zoom_start, tiles=None)

    # OS Map layer
    os_map_url = f'https://api.os.uk/maps/raster/v1/zxy/Light_3857/{{z}}/{{x}}/{{y}}.png?key={api_key}'
    folium.TileLayer(
        tiles=os_map_url,
        attr='Ordnance Survey',
        name='Ordnance Survey Map',
        overlay=False,
        control=True
    ).add_to(m)

    # Add OpenStreetMap as an alternative layer
    folium.TileLayer('OpenStreetMap', name="OpenStreetMap").add_to(m)

    # Layer control
    folium.LayerControl().add_to(m)

    # Save the map to an HTML file
    m.save('index.html')

    # Custom HTML to include search functionality using OS Names API
    search_html = f"""
    <form>
        <input type="text" id="searchBox" placeholder="Enter a location">
        <button type="button" onclick="searchLocation()">Search</button>
    </form>
    <script>
    function searchLocation() {{
        var searchText = document.getElementById('searchBox').value;
        var url = "https://api.os.uk/search/names/v1/find?query=" + encodeURIComponent(searchText) + "&key={names_api_key}";

        fetch(url)
            .then(response => response.json())
            .then(data => {{
                if(data.results && data.results.length > 0) {{
                    var loc = data.results[0].geometry.coordinates;
                    var map = L.map('map').setView([loc[1], loc[0]], 10);
                    L.marker([loc[1], loc[0]]).addTo(map).bindPopup(searchText).openPopup();
                }} else {{
                    alert('Location not found.');
                }}
            }})
            .catch(error => alert('Error: ' + error));
    }}
    </script>
    """
    with open("index.html", "a") as map_file:
        map_file.write(search_html)

    print("OS Map with search functionality has been saved to 'UK_OS_Map.html'")
    
# Replace these with your actual API keys
api_key = 'aFVNHAYfAZgEsTb5g26B4v2JcVRsCzjl'
names_api_key = 'aFVNHAYfAZgEsTb5g26B4v2JcVRsCzjl'
create_os_map(api_key, names_api_key)