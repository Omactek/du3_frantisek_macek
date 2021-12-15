import json
import os

kont_coord = []
kont_id = []

try:
    if os.path.getsize("kontejnery.geojson") == 0:
        print("Vstupní soubor je prázdný")
        quit()
except FileNotFoundError:
    print("Chybí vstupní soubor")
    quit()

with open("kontejnery.geojson", encoding="utf8") as kinfile:
        kontejnery = json.load(kinfile)

for feature in kontejnery['features']:
    kont_coord.append([feature["geometry"]["coordinates"][1],feature["geometry"]["coordinates"][1],feature["properties"]["STATIONNAME"],feature["properties"]["PRISTUP"]])

print(kont_coord)




