import json
import os
from pyproj import Transformer

kont = [] #[[x,y,stationname,pristup]]
kont_volne = []
adr = []
adr_krovak = []
kontejnery_path = "kontejnery.geojson"
adresy_path = "adresy.geojson"

def load_file(file_path, file, file_name): #načte vstupní soubor a ověří, jestli existuje, nebo je prázdný
    try:
        if os.path.getsize(file_path) == 0:
            print(f"Vstupní soubor {file} je prázdný.")
            quit()
    except FileNotFoundError:
        print(f"Chybí vstupní soubor {file}.")
        quit()
    with open("kontejnery.geojson", encoding="utf8") as file_name:
        kontejnery = json.load(file_name)
        return kontejnery

#načtení vstupního souboru kontejnerů
kontejnery = load_file(kontejnery_path, "kontejnery", "kinfile") #načte vstupní soubor a ověří, jestli existuje, nebo je prázdný

for feature in kontejnery["features"]: #načte do listu jen relevatní položky
    kont.append([feature["geometry"]["coordinates"][1],feature["geometry"]["coordinates"][1],feature["properties"]["STATIONNAME"],feature["properties"]["PRISTUP"]])

for i in range(len(kont)): #zvolí jen volně dostupné kontejnery
    if kont[i][3] == "volně":
        kont_volne.append(kont[i][0:3])

#načtení vstupního souboru adres
adresy = load_file(adresy_path, "adresy", "adinfile")

for feature in adresy["features"]:
    adr.append([feature["geometry"]["coordinates"][1],feature["geometry"]["coordinates"][2],feature["properties"]["addr:housenumber"],feature["properties"]["addr:street"]])

print(adr)