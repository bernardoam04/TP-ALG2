import requests
import folium
from osm2geojson import json2geojson


user_agent = 'Mozilla/5.0'
overpass_url = "http://overpass-api.de/api/interpreter"

overpass_query = """
[out:json];
area["name"="Belo Horizonte"][admin_level=8]->.a;
(
  rel["admin_level"="9"](area.a);
);
out body;
>;
out skel qt;
"""

# requisicao api 
response = requests.get(overpass_url, params={'data': overpass_query}, headers={'User-Agent': user_agent})
data = response.json()

# converter para dados de geo 
geojson_data = json2geojson(data)

# cria o mapa 
m = folium.Map(location=[-19.92, -43.94], zoom_start=12, tiles='Stamen Toner')

#add os disitritos 
folium.GeoJson(
    geojson_data,
    name='Distritos de BH'
).add_to(m)

folium.LayerControl().add_to(m)
m.save("mapa_bh_distritos.html")
