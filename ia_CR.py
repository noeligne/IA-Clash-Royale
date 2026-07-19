#!/usr/bin/env python3
import random
import csv
from settings import *
from cartes import *
from db_management import *
from pull_deck import *
from synergy import *

if (input("Do you wish to enable online mode (y/n)").startswith("y")):
    print("this option is not yet available...")
    #import clash_royale
    #from dotenv import load_dotenv
    #import os

    #load_dotenv()
    #API_KEY = os.getenv("API_KEY")
    #client = clash_royale.Client(api_key = API_KEY)
    LOCAL_MODE = True
else:
    LOCAL_MODE = True

class Main:
    def __init__(self):
        self.setting = Settings()
        self.collection = Collection()
        self.local = LOCAL_MODE
        self.setting.set_main(self, self.local)
        self.db = ""
        self.preset_name = ""
        self.synergy = Synergies()
        self.battlelog = None
    
    def start(self):
        with open("./global/presets.csv", newline='', encoding="utf-8") as csvfile:
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
        while True:
            bdd = load_bdd(self.db)
            bdd = sync_preset(self, bdd)
            self.collection.update(bdd)
            load_synergy(self.synergy, self.collection)
            menu = input("Would you like to generate a deck, play triple draft mode or go to the settings ? (1, 2 or 3)\n")
            if menu == "1" or menu == "2":
                if menu == "1":
                    deck = tirage_aleatoire(self.collection, self.setting, self.synergy)
                else:
                    deck = triple_draft_mode(self.collection, self.setting, self.synergy)
                deck.affiche()
                win = int(input("How many towers did you destroy ? "))
                loose = int(input("How many of your towers got destroyed ? "))
                if win - loose < 0:
                    score = win - (loose * (1 - 0.1 * win ))
                else:
                    score = win - loose
                deck.gagne(score, self.collection.avg_score(), self.setting.m_elixir)
                deck.update_deck_synergy(score, self.synergy)
            elif menu == "3" :
                self.setting.settings()
            save_bdd(self.collection, self.db)
            save_synergy(self.synergy)

    def load_preset(self):
        with open("./global/presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                print(row[0] + "\n")
            name = input("Choose the preset you want to load\n")
        with open("./global/presets.csv", newline='', encoding="utf-8") as csvfile:
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
                    if (not LOCAL_MODE):
                        try:
                            if (row[5] != "" and row[5] != None):
                                self.setting.set_player(True, row[5])
                        except:
                            print("No player tag found...")
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
        if (input("would you like to connect the preset to your Clash Royale account ?").startswith("y")):
            self.setting.set_player()
        with open("./global/presets.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([name, str(self.setting.m_elixir), db_name, ban, self.setting.heros, self.setting.player_tag])
    
    def save_preset(self):
        local_save = [[self.preset_name, str(self.setting.m_elixir), self.db, self.setting.get_banned_cars_str(), self.setting.heros, self.setting.player_tag]]
        with open("./global/presets.csv", "r", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if row[0] != local_save[0][0]:
                    preset = row
                    local_save.append(preset)
        with open("./global/presets.csv", "w", newline='', encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["name", "avg_elixir", "db_name", "banned_cards", "heros_slot", "player_tag"])
            for preset in local_save:
                writer.writerow(preset)
        print(f"{self.preset_name} Successfully saved !\n")

class Collection:
    def __init__(self):
        self.collection = []
    
    def ajoutecarte(self, nom, ratio, heros, elixir, level):
        for carte in self.collection:
            if carte.nom == nom:
                if carte.ratio != ratio:
                    carte.ratio = ratio
                return
        self.collection.append(Carte(nom, ratio, heros, elixir, level))
    
    def update(self, bdd):
        bdd = sorted(bdd)
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
    
    def reset_final_ratio(self):
        for carte in self.collection:
            carte.final_ratio = carte.ratio
    
    def get_card(self, name):
        for card in self.collection:
            if (card.nom == name):
                return card
        return None
    
    def get_cards(self):
        l = []
        for card in self.collection:
            l.append(card.nom)
        return l

input("Welcome to the Clash Royale smart deck draw ! (press enter)")
app = Main()
app.start()