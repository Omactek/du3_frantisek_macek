import json
import os
from pyproj import Transformer
from math import sqrt
from statistics import median

kont = [] #[[x,y,stationname,pristup]]
kont_volne = [] #[[x,y,stationname]]
adr = [] #[[x,y,housenumber,street]]
kontejnery_path = "kontejnery.geojson"
adresy_path = "adresy.geojson"
adresa_vzdalenost = [] #[[vzdalenost, housenumber, street]]
avg_dist = 0 #prumerna vzdalenost
med_dist = 0 #median vzdalenosti
max_dist = [0] #[vzdálenost, housenumber, street]


def load_file(file_path, file): #načte vstupní soubor a ověří, jestli existuje, nebo je prázdný
    try:
        if os.path.getsize(file_path) == 0:
            print(f"Vstupní soubor {file} je prázdný.")
            quit()
    except FileNotFoundError:
        print(f"Chybí vstupní soubor {file}.")
        quit()
    try:    
        with open(file_path, encoding="utf8") as file_name:
            data = json.load(file_name)
            return data
    except ValueError:
        print(f"Vadný formát souboru {file}.")
        quit()

def euclidean_distance(coord_1_x,coord_1_y,coord_2_x, coord_2_y): #funkce na vypočítání vzdálenosti
    distance = pow(pow(coord_1_x - coord_2_x, 2) + pow(coord_1_y - coord_2_y, 2),0.5)
    return distance

def average(list, position): #funkce na vypočítání průměru z listu listů
    avg = sum(x[position] for x in list) / len(list)
    return avg

def med_lol(list, position): #funkce na vypočítání mediánu z listu listů
    med = median(x[position] for x in list)
    return med

def check_distance(list,value): #funkce kontroluje, jestli není minimální vzdálenost moc velká
    if any(num > value for num in (x[0] for x in list)) == True:
        print(f"Minimální vzdálenost jednoho z adresních bodů je více než {value} m.\nKonec programu.")
        quit()

#načtení vstupního souboru kontejnerů
kontejnery = load_file(kontejnery_path, "kontejnery") #načte vstupní soubor a ověří, jestli existuje, nebo je prázdný

for feature in kontejnery["features"]: #načte do listu jen relevatní položky
    kont.append([feature["geometry"]["coordinates"][0],feature["geometry"]["coordinates"][1],feature["properties"]["STATIONNAME"],feature["properties"]["PRISTUP"]])

for i in range(len(kont)): #zvolí jen volně dostupné kontejnery
    if kont[i][3] == "volně":
        kont_volne.append(kont[i][0:3])

#načtení vstupního souboru adres
adresy = load_file(adresy_path, "adresy")

for feature in adresy["features"]: #načte do listu jen relevatní položky
    adr.append([feature["geometry"]["coordinates"][0],feature["geometry"]["coordinates"][1],feature["properties"]["addr:housenumber"],feature["properties"]["addr:street"]])

#převedení souřadnic do s-jtsk
wgs84_sjtsk = Transformer.from_crs("epsg:4326","epsg:5514")
for i in range(len(adr)):
    adr[i][0] = wgs84_sjtsk.transform(adr[i][1],adr[i][0])
    adr[i][1] = adr[i][0][1]
    adr[i][0] = adr[i][0][0]

#vypočítání vzdálenosti
for i in range(len(adr)):
    adresa_vzdalenost.append([euclidean_distance(adr[i][0],adr[i][1],kont_volne[0][0],kont_volne[0][1]),adr[i][2],adr[i][3]])
    for z in range(len(kont_volne)):
        temp_dist = euclidean_distance(adr[i][0],adr[i][1],kont_volne[z][0],kont_volne[z][1])
        if temp_dist < adresa_vzdalenost[i][0]:
            adresa_vzdalenost[i][0] = temp_dist

#kontrola velikosti vzdáleností
check_distance(adresa_vzdalenost,10000)

#vypočet průměru
avg_dist = int(round(average(adresa_vzdalenost,0)))

#vypočet mediánu
med_dist = int(round(med_lol(adresa_vzdalenost,0)))

#zjištění maximální vzdálenosti
for i in range(len(adresa_vzdalenost)):
    if max_dist[0] < adresa_vzdalenost[i][0]:
        max_dist = adresa_vzdalenost[i]
max_dist[0] = int(round(max_dist[0],0))

#výpis informací
print(f"Načteno {len(adr)} adresních bodů.\nNačteno {len(kont)} kontejnerů na tříděný odpad.\n")
print(f"Průměrná vzdálenost ke kontejneru je {avg_dist} m.\nMediánová vzdálenost ke kontejneru je {med_dist} m.\n")
print(f"Nejdále ke kontejneru je z adresy {max_dist[2]} {max_dist[1]} a to {max_dist[0]} m.")