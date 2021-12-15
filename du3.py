import json
import os

kont = []
kont_volne = []

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
    kont.append([feature["geometry"]["coordinates"][1],feature["geometry"]["coordinates"][1],feature["properties"]["STATIONNAME"],feature["properties"]["PRISTUP"]])

for i in range(len(kont)):
    if kont[i][3] == "volně":
        kont_volne.append(kont[i][0:3])

print(len(kont),len(kont_volne))


