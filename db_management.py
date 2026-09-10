import csv
from synergy import *
from cartes import *

def save_bdd(collection, filename="static/base_de_donnee.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nom", "ratio", "level"])
        for carte in sorted(collection.collection, key=lambda x:x.nom):
            writer.writerow([carte.nom, carte.ratio, carte.level])

def load_bdd(filename = "static/base_de_donnee.csv"):
    liste = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            liste.append([row[0],float(row[1]), int(row[2])])
    return liste

def save_synergy(synergies, filename="global/synergies.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["card1", "card2", "win", "lose"])
        for synergy in synergies.synergies:
            writer.writerow([synergy.first.nom, synergy.second.nom, synergy.win, synergy.lose])

def load_synergy(synergies, collection, filename = "global/synergies.csv"):
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            synergies.add_synergy(collection.get_card(row[0]), collection.get_card(row[1]), int(row[2]), int(row[3]))

def sync_preset(main, bdd):
    existing_cards = main.collection.get_cards()
    for card in CARDS_STATIC.data.keys():
        if card not in existing_cards:
            bdd.append([card, 1, 16])
            print(f"New card added : {CARDS_STATIC.data[card]["name"][main.setting.lang]}")
    return bdd