#!/usr/bin/env python3
import json
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
        self.preset = Config("./global/presets.json")
    
    def start(self):
        if self.preset.data:
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
                win = -1
                while win < 0:
                    try :
                        win = int(input("How many towers did you destroy ? "))
                        loose = int(input("How many of your towers got destroyed ? "))
                    except :
                        print("Please enter a number")
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
        name = ""
        while name not in self.preset.data.keys() :
            for sets in self.preset.data.keys():
                print(f"- {sets}")
            name = input("Choose the preset you want to load\n")
        self.preset_name = name
        self.db = self.preset.data[name]["db_name"]
        self.collection.update(load_bdd(self.db))
        print("Database loaded succesfully\n")
        self.setting.banlist = []
        if not self.preset.data[name]["ban"] == []:
            self.setting.exclusion(self.preset.data[name]["ban"])
        self.setting.m_elixir = self.preset.data[name]["avg_elixir"]
        print(f"Average elixir set to {self.setting.m_elixir}")
        self.setting.heros = self.preset.data[name]["heros_slots"]
        print(f"Heros slots set to {self.setting.heros}\n")
        print(f"\"{name}\" Successfully loaded !\n")
        if (not LOCAL_MODE):
            try:
                if (self.preset.data[name]["player_tag"] != ""):
                    self.setting.set_player(True, self.preset.data[name]["player_tag"])
            except:
                print("No player tag found...")
        return self.main_menu()

    def create_preset(self):
        name = input("How would you like to call your new preset ?\n")
        db_name = "./databases/" + name + ".csv"
        self.setting.change_avg_elixir(True)
        self.setting.heros_slot(True)
        bdd = load_bdd()
        self.collection.update(bdd)
        save_bdd(self.collection, db_name)
        self.db = db_name
        self.preset_name = name
        if (input("would you like to connect the preset to your Clash Royale account ?").startswith("y")):
            self.setting.set_player()
        self.preset.data[name] = {"avg_elixir" : self.setting.m_elixir,
                             "db_name" : db_name,
                             "ban" : [],
                             "heros_slots" : self.setting.heros,
                             "player_tag" : self.setting.player_tag}
        self.preset.save()
    
    def save_preset(self):
        self.preset.data[self.preset_name]["avg_elixir"] = self.setting.m_elixir
        self.preset.data[self.preset_name]["ban"] = [card.nom for card in self.setting.banlist]
        self.preset.data[self.preset_name]["heros_slots"] = self.setting.heros
        self.preset.data[self.preset_name]["player_tag"] = self.setting.player_tag
        self.preset.save()
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