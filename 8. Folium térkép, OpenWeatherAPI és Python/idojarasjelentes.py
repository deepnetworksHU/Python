import requests
import json
import folium
import yaml

config = yaml.load(open("settings.yaml", encoding="utf8"))

apikey = config["apikey"]
egyseg = config["egyseg"]

start = config["start"]

r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={start}&appid={apikey}&units=metric&lang=hu")
jsonformatum = json.loads(r.text)

lat = jsonformatum["coord"]["lat"]
lon = jsonformatum["coord"]["lon"]

cél = config["cél"]

r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={cél}&appid={apikey}&units=metric&lang=hu")
jsonformatum = json.loads(r.text)

cel_lat = jsonformatum["coord"]["lat"]
cel_lon = jsonformatum["coord"]["lon"]

lat_valtozas= (cel_lat-lat) / egyseg
lon_valtozas = (cel_lon - lon) / egyseg

m = folium.Map(location=[lat,lon], zoom_start=6)

for i in range(egyseg + 1):
    
    r = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apikey}&units=metric")
    jsonformatum = json.loads(r.text)

    icon = jsonformatum["weather"][0]["icon"]
    idojaras_icon = folium.features.CustomIcon('http://openweathermap.org/img/wn/' + icon + '.png', icon_size=(50,50))

    homerseklet = jsonformatum["main"]["temp"]
    folium.Marker([lat,lon],icon=folium.DivIcon(
        html=f"""<div style="font-family: Arial; font-size: 30px;color: {'lightblue' if homerseklet < 5 else 'gray'}">{"{:.0f}".format(homerseklet)}</div>"""
    )).add_to(m)
    folium.Marker([lat+0.3,lon],icon=idojaras_icon).add_to(m)
    lat += lat_valtozas
    lon += lon_valtozas

m.save("map.html")