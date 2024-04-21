import folium

def create_os_map(api_key, center=(54.5, -4), zoom_start=6):
    # Initialize the map centered around the UK
    m = folium.Map(location=center, zoom_start=zoom_start)

    # Ensure the tile URL is compatible with EPSG:3857
    # Example URL (please verify with the documentation or OS support for the correct URL):
    os_map_url = f'https://api.os.uk/maps/raster/v1/zxy/Light_3857/{{z}}/{{x}}/{{y}}.png?key={api_key}'

    # Add the Ordnance Survey map layer that supports Web Mercator (EPSG:3857)
    os_map = folium.TileLayer(
        tiles=os_map_url,
        attr='Ordnance Survey',
        name='Ordnance Survey Map',
        overlay=False,
        control=True
    )
    os_map.add_to(m)

    # Optionally, add OpenStreetMap as an alternative layer
    folium.TileLayer('OpenStreetMap', name="OpenStreetMap").add_to(m)

    # Add layer control to toggle on/off
    folium.LayerControl().add_to(m)

    return m

# Replace 'your_api_key_here' with your actual Ordnance Survey API key
api_key = 'your_api_key_here'
uk_os_map = create_os_map(api_key)

# Save the map to an HTML file
uk_os_map.save('index.html')

print("OS Map has been saved to 'index.html'")