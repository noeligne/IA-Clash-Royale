#!/usr/bin/env python3
import random
import csv
from settings import *
from cartes import *
from db_management import *
from pull_deck import *

class Main:
    def __init__(self):
        self.setting = Settings()
        self.collection = Collection()
        self.setting.set_main(self)
        self.db = ""
        self.preset_name = ""
    
    def start(self):
        with open("./static/presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            if sum(1 for line in csvfile) > 1:
                menu = input("Would you like to load or create a preset ? (1 or 2)\n")
                if menu == "1":
                    self.load_preset()
                else :
                    self.create_preset()
            else :
                print("No existing preset found\n")
                self.create_preset()
        self.main_menu()
    
    def main_menu(self):
        bdd = load_bdd(self.db)
        self.collection.update(bdd)
        menu = input("Souhaitez-vous tirer une carte ou aller dans les paramètres ? (1 ou 2)\n")
        if menu == "1":
            deck = tirage_aleatoire(self.collection, self.setting)
            deck.affiche()
            win = int(input("Combien de tour avez vous détruites ? "))
            loose = int(input("Combien de vos tours ont été détruites ? "))
            if win - loose < 0:
                score = win - (loose * (1 - 0.1 * win ))
            else:
                score = win - loose
            deck.gagne(score, self.collection.avg_score(), self.setting.m_elixir)
        elif menu == "2" :
            self.setting.settings()
        print()
        save_bdd(self.collection, self.db)
        self.main_menu()
    
    def load_preset(self):
        with open("./static/presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                print(row[0] + "\n")
            name = input("Choose the preset you want to load\n")
        with open("./static/presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if row[0] == name :
                    self.preset_name = name
                    self.db = row[2]
                    self.collection.update(load_bdd(self.db))
                    print("Database loaded succesfully\n")
                    if row[3] != "":
                        self.setting.exclusion(row[3].split(";"))
                    else:
                        self.setting.banlist = []
                    self.setting.m_elixir = float(row[1])
                    print(f"Average elixir set to {self.setting.m_elixir}")
                    try:
                        self.setting.heros = float(row[4])
                    except:
                        self.setting.heros = 1
                    print(f"Heros slots set to {self.setting.heros}\n")
                    print(f"\"{name}\" Successfully loaded !\n")
                    return self.main_menu()
        print(f"\"{name}\" Didn't load")
        return self.start()

    def create_preset(self):
        name = input("How would you like to call your new preset ?\n")
        db_name = "./databases/" + name + ".csv"
        self.setting.change_avg_elixir(True)
        self.setting.heros_slot(True)
        ban = ""
        with open(db_name, 'w') as f:
            writer = csv.writer(f)
        bdd = load_bdd()
        self.collection.update(bdd)
        save_bdd(self.collection, db_name)
        self.db = db_name
        self.preset_name = name
        with open("./static/presets.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, str(self.setting.m_elixir), db_name, ban, self.setting.heros])
    
    def save_preset(self):
        local_save = [[self.preset_name, str(self.setting.m_elixir), self.db, self.setting.get_banned_cars_str(), self.setting.heros]]
        with open("./static/presets.csv", "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if row[0] != local_save[0][0]:
                    preset = row
                    local_save.append(preset)
        with open("./static/presets.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "avg_elixir", "db_name", "banned_cards", "heros_slot"])
            for preset in local_save:
                writer.writerow(preset)
        print(f"{self.preset_name} Successfully saved !\n")

class Collection:
    def __init__(self):
        self.collection = []
    
    def ajoutecarte(self, nom, ratio, heros, elixir, level):
        for carte in self.collection:
            if carte.nom == nom:
                return
        self.collection.append(Carte(nom, ratio, heros, elixir, level))
    
    def update(self, bdd):
        for carte in bdd:
            self.ajoutecarte(carte[0], carte[1], carte[2], carte[3], carte[4])
        
    def total_score(self):
        score = 0
        for carte in self.collection:
            if not carte.banned:
                score += carte.ratio
        return score
    
    def len_collection(self):
        c = 0
        for carte in self.collection:
            if not carte.banned:
                c += 1
        return c
    
    def avg_score(self):
        return self.total_score() / self.len_collection()

input("Bonjour bienvenue dans le tirage aléatoire intelligent de deck clash royale ! (appuyez sur entrée)")
app = Main()
app.start()