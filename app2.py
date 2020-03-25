import folium
import pandas

dataVol = pandas.read_csv("Volcanoes.txt")
map = folium.Map(location = [44.196037, 17.918107], zoom_start=1, tiles = "Stamen Terrain")

htmls = """<h4>Volcano information:</h4>
 Location: %s\n
 Current status: %s
 """

lat = list(dataVol["LAT"])
print(lat)
lon = list(dataVol["LON"])
loc = list(dataVol["LOCATION"])
stat = list(dataVol["STATUS"])
elev = list(dataVol["ELEV"])

def putColor(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000<= elevation < 3000:
        return 'orange'
    else:
        return 'red'

fgv = folium.FeatureGroup(name = "Volcanoes") #feature Group for volcanoes

for latX, lonY, locZ, statW, el in zip(lat, lon, loc, stat, elev):
    iframe = folium.IFrame(html=htmls % (locZ, statW), width=200, height=100)
    fgv.add_child(folium.Marker(location = [latX, lonY], popup=folium.Popup(iframe),
    icon = folium.Icon(color = putColor(el), icon = 'cloud' )))

fgp = folium.FeatureGroup(name = "Population")

fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding='utf-8-sig').read(),
style_function= lambda x: {'fillColor' : 'red' if x['properties']['POP2005'] < 5000000
else 'yellow' if 5000000 <= x['properties']['POP2005'] < 12000000 else 'green' }))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")