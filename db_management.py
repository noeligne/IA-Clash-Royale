import csv
from synergy import *
from cartes import *
import json

def save_bdd(collection, filename="static/base_de_donnee.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nom", "ratio", "heros", "elixir", "level"])
        for carte in collection.collection:
            writer.writerow([carte.nom, carte.ratio, str(carte.heros), carte.elixir, carte.level])

def load_bdd(filename = "static/base_de_donnee.csv"):
    liste = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if row[2] == "False":
                liste.append([row[0],float(row[1]),False, int(row[3]), int(row[4])])
            else:
                liste.append([row[0],float(row[1]),True, int(row[3]), int(row[4])])
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
    l = main.collection.get_cards()
    with open("./static/base_de_donnee.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if row[0] not in l:
                if row[2] == "False":
                    bdd.append([row[0],float(row[1]),False, int(row[3]), int(row[4])])
                else:
                    bdd.append([row[0],float(row[1]),True, int(row[3]), int(row[4])])
    bdd = sorted(bdd)
    return bdd

class Config:
    def __init__(self, filename):
        self.filename = filename
        self.data = {}

        with open(filename, encoding="utf-8") as f:
            self.data = json.load(f)

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4)