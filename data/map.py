import requests
import folium
from osm2geojson import json2geojson

#conectar API
user_agent = 'Mozilla/5.0'
overpass_url = "http://overpass-api.de/api/interpreter"

# consulta dos distritos 
overpass_query_distritos = """
[out:json];
area["name"="Belo Horizonte"][admin_level=8]->.a;
(
  rel["admin_level"="9"](area.a);
);
out body;
>;
out skel qt;
"""

#adicao das ruas 
overpass_query_ruas = """
[out:json];
area["name"="Belo Horizonte"][admin_level=8]->.a;
way["highway"](area.a);
out body;
>;
out skel qt;
"""

# query dos distritos e ruas 
resp_distritos = requests.get(overpass_url, params={'data': overpass_query_distritos}, headers={'User-Agent': user_agent})
geojson_distritos = json2geojson(resp_distritos.json())
resp_ruas = requests.get(overpass_url, params={'data': overpass_query_ruas}, headers={'User-Agent': user_agent})
geojson_ruas = json2geojson(resp_ruas.json())

# mapa 
m = folium.Map(location=[-19.92, -43.94], zoom_start=13, tiles='CartoDB Positron')
folium.GeoJson(
    geojson_distritos,
    name='Distritos',
    style_function=lambda x: {'color': 'green', 'fillOpacity': 0.1, 'weight': 1}
).add_to(m)

folium.GeoJson(
    geojson_ruas,
    name='Ruas',
    style_function=lambda x: {'color': 'blue', 'weight': 0.8}
).add_to(m)

# parte interativ de controle de camadas
folium.LayerControl().add_to(m)

m.save("mapa_bh_com_ruas.html")
print("Mapa salvo como mapa_bh_com_ruas.html")
