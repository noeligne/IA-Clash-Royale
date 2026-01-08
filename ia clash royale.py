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
        with open("static\presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            if sum(1 for line in csvfile) > 1:
                menu = input("Would you like to load or create a preset ? (1 or 2)\n")
                if menu == "1":
                    with open("static\presets.csv", newline='', encoding="utf-8") as csvfile:
                        reader = csv.reader(csvfile)
                        next(reader)
                        for row in reader:
                            print(row[0] + "\n")
                        return self.load_preset(input("Choose the preset you want to load\n"))
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
    
    def load_preset(self, name):
        with open("static\presets.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader) 
            for row in reader:
                if row[0] == name :
                    self.preset_name = name
                    self.db = row[2]
                    self.setting.m_elixir = float(row[1])
                    print(f"\"{name}\" Successfully loaded !\n")
                    return self.main_menu()
        print(f"\"{name}\" Didn't load")
        return self.start()

    def create_preset(self):
        name = input("How would you like to call your new preset ?\n")
        db_name = "./databases/" + name + ".csv"
        self.setting.change_avg_elixir()
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
            writer.writerow([name, str(self.setting.m_elixir), db_name, ban])

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
    def __init__(self,banlist=[]):
        self.deck = []
        self.banlist= banlist
        self.maxi = 0
    
    def plein(self):
        return len(self.deck) == 8
    
    def ajoute_carte(self, carte):
        if self.plein():
            return
        if carte.heros:
            for c in self.deck:
                if c.heros:
                    return
        if carte in self.deck:
            return
        if carte in self.banlist:
            return
        self.deck.append(carte)
    
    def vide_deck(self):
        self.deck = []
    
    def gagne(self, score, avg_score, m_elixir):
        coeff = score
        for carte in self.deck:
            if score > 0 :
                ecart_avg_elixir = m_elixir - self.avg_elixir()
                if ecart_avg_elixir < 0:
                    ecart_avg_elixir *= -1
                coeff = score * (1 + ((avg_score - carte.ratio) / avg_score)) * (1 + (1 / (1 + ecart_avg_elixir)) * 0.2)
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
    deck = Deck(setting.banlist)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights=[c.ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        pool.remove(carte)
    return deck

input("Bonjour bienvenue dans le tirage aléatoire intelligent de deck clash royale ! (appuyez sur entrée)")
app = Main()
app.start()