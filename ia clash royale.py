import random
import csv


class Collection:
    def __init__(self):
        self.collection = []
        self.banlist = []
    
    def ajoutecarte(self, nom, ratio, heros, elixir):
        for carte in self.collection:
            if carte.nom == nom:
                return
        self.collection.append(Carte(nom,ratio,heros, elixir))
    
    def update(self, bdd):
        for carte in bdd:
            self.ajoutecarte(carte[0],carte[1],carte[2], carte[3])
        
    def exclusion(self):
        print("choisis la carte à bannir :")
        for carte in self.collection:
            if carte not in self.banlist:
                print(carte.nom)
        ban = input()
        for carte in self.collection:
            if carte.nom == ban:
                self.banlist.append(carte)
                return

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
    
    def plein(self):
        return len(self.deck) == 8
    
    def ajoute_carte(self,carte):
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
        return maxi
    
    def affiche(self):
        if self.plein():
            print(f"/{self.deck[0].nom} | {self.deck[1].nom} | {self.deck[2].nom} | {self.deck[3].nom}\ \n\{self.deck[4].nom} | {self.deck[5].nom} | {self.deck[6].nom} | {self.deck[7].nom}/")

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

class Carte:
    def __init__(self,nom, ratio, heros, elixir):
        self.nom = nom
        self.ratio = ratio
        self.heros = heros
        self.elixir = elixir
    
    def ajoutescore(self,score):
        if self.ratio+score >= 1:
            self.ratio += score
        else :
            self.ratio = 1

def load_bdd():
    liste = []
    with open("base_de_donnee.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader) 
        for row in reader:
            if row[2] == "False":
                liste.append([row[0],float(row[1]),False, int(row[3])])
            else:
                liste.append([row[0],float(row[1]),True, int(row[3])])
    return liste

def save_bdd(collection, filename="base_de_donnee.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["nom", "ratio", "heros", "elixir"])
        for carte in collection.collection:
            writer.writerow([carte.nom, carte.ratio, str(carte.heros), carte.elixir])

def tirage_aleatoire(collection):
    deck = Deck(collection.banlist)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights=[c.ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        pool.remove(carte)
    return deck

input("Bonjour bienvenue dans le tirage aléatoire intelligent de deck clash royale ! (appuyez sur entrée)")
c = Collection()
m_elixir = 3.5
while True :
    bdd = load_bdd()
    c.update(bdd)
    menu = input("souhaitez vous tirer, exclure une carte ou aller dans les paramètres ? (1, 2 ou 3)")
    if menu == "2":
        c.exclusion()
    elif menu == "1":
        deck = tirage_aleatoire(c)
        deck.affiche()
        win = int(input("Combien de tour avez vous détruites?"))
        loose = int(input("Combien de vos tours ont étés détruites ?"))
        if win - loose < 0:
            score = win - (loose * (1 - 0.1 * win ))
        else :
            score = win - loose
        deck.gagne(score, c.avg_score(), m_elixir)
    elif menu == "3" :
        print("\n Menu des paramètres :\n1 - moyenne elixir\n(sélectionnez le numéro correspondant au paramètre désiré)")
        param = input()
        if param == "1":
            print("\nvers quelle valeur voulez vous que la moyenne du coût d'elixir tende ? \n(de base = 3.5)")
            m_elixir = float(input())
            if m_elixir < 0:
                m_elixir = -m_elixir
            if m_elixir > 7.1:
                m_elixir = 7.1
            print("La moyenne tendra donc vers : ", m_elixir)
    print()
    save_bdd(c)