#!/usr/bin/env python3
import random
import csv
from settings import *
from cartes import *

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
    
    def ajoutecarte(self, nom, ratio, heros, elixir):
        for carte in self.collection:
            if carte.nom == nom:
                return
        self.collection.append(Carte(nom, ratio, heros, elixir))
    
    def update(self, bdd):
        for carte in bdd:
            self.ajoutecarte(carte[0], carte[1], carte[2], carte[3])
        
    def total_score(self):
        score = 0
        for carte in self.collection:
            score += carte.ratio
        return score
    
    def avg_score(self):
        return self.total_score() / len(self.collection)

class Deck:
    def __init__(self, setting):
        self.deck = []
        self.banlist= setting.banlist
        self.maxi = 0
        self.heros = 0
        self.setting = setting
    
    def plein(self):
        return len(self.deck) == 8
    
    def ajoute_carte(self, carte):
        if self.plein():
            return
        if carte.heros:
            if self.heros == self.setting.heros:
                return
        if carte in self.deck:
            return
        if carte in self.banlist:
            return
        if carte.heros:
            self.heros += 1
        self.deck.append(carte)
    
    def vide_deck(self):
        self.deck = []
        self.heros = 0
    
    def gagne(self, score, avg_score, m_elixir):
        coeff = score
        for carte in self.deck:
            if score > 0 :
                ecart_avg_elixir = m_elixir - self.avg_elixir()
                if ecart_avg_elixir < 0:
                    ecart_avg_elixir *= -1
                ratio_percentage = (1 + ((avg_score - carte.ratio) / avg_score))
                if ratio_percentage <= 0:
                    ratio_percentage = 0.01
                coeff = score * ratio_percentage * (1 + (1 / (1 + ecart_avg_elixir)) * 0.2) * 1.2
            else :
                coeff = score * (1 + ((carte.ratio - avg_score) / avg_score))
            carte.ajoutescore(coeff)

    def plus_caractere(self):
        if len(self.deck) == 0:
            return 0
        maxi = len(self.deck[0].nom)
        for carte in self.deck:
            if len(carte.nom) > maxi:
                maxi = len(carte.nom)
        self.maxi = maxi
    
    def affiche(self):
        string = ""
        index = 0
        separator = ["/", "|", "|", "|", "\\\n\\", "|", "|", "|", "/"]
        self.plus_caractere()
        if self.plein():
            for i in range(8):
                string += separator[i]
                middle = round((self.maxi + 2 - len(self.deck[index].nom))/2)
                if len(self.deck[index].nom) < self.maxi :
                    if (self.maxi - len(self.deck[index].nom)) % 2 == 0:
                        string += " " * middle + str(self.deck[index].nom) + " " * middle
                    elif middle > (self.maxi + 2 - len(self.deck[index].nom))/2 :
                        string += " " * (middle - 1) + str(self.deck[index].nom) + " " * middle
                    else :
                        string += " " * middle + str(self.deck[index].nom) + " " * (middle + 1)
                else :
                    string += " " + str(self.deck[index].nom) + " "
                index += 1
            string += separator[i + 1] + "\n"
            print(string)

    def avg_elixir(self):
        nb = 0
        elixir = 0
        for carte in self.deck :
            elixir += carte.elixir
            nb += 1
        if nb > 0:
            return elixir / nb
        else:
            return 0

def load_bdd(filename = "static/base_de_donnee.csv"):
    liste = []
    with open(filename, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if row[2] == "False":
                liste.append([row[0],float(row[1]),False, int(row[3])])
            else:
                liste.append([row[0],float(row[1]),True, int(row[3])])
    return liste

def save_bdd(collection, filename="static/base_de_donnee.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nom", "ratio", "heros", "elixir"])
        for carte in collection.collection:
            writer.writerow([carte.nom, carte.ratio, str(carte.heros), carte.elixir])

def tirage_aleatoire(collection, setting):
    deck = Deck(setting)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights=[c.ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        pool.remove(carte)
    return deck

input("Bonjour bienvenue dans le tirage aléatoire intelligent de deck clash royale ! (appuyez sur entrée)")
app = Main()
app.start()