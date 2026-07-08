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
                ratio_percentage = (1 + ((avg_score - carte.ratio) / avg_score))
                if ratio_percentage <= 0:
                    ratio_percentage = 0.01
                coeff = score * ratio_percentage * 1.2 * (carte.level / 16)
            else :
                coeff = score * (1 + ((carte.ratio - avg_score) / avg_score)) * 0.75 * (carte.level / 16)
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
    
    def elixir_sum(self):
        elixir = 0
        for carte in self.deck:
            elixir += carte.elixir
        return elixir
    
    def is_card_in_deck(self, nom):
        for carte in self.deck:
            if (carte.nom == nom):
                return True
        return False

    def update_deck_synergy(self, score, synergies):
        for i in range(len(self.deck)):
            for j in range(i + 1, len(self.deck), 1):
                synergies.update_synergy(self.deck[i], self.deck[j], score)

class Carte:
    def __init__(self, nom, ratio, heros, elixir, level=16):
        self.nom = nom
        self.ratio = ratio
        self.final_ratio = ratio
        self.heros = heros
        self.elixir = elixir
        self.banned = False
        self.level = level
    
    def ajoutescore(self, score):
        if self.ratio + score >= 1:
            self.ratio += score
        else :
            self.ratio = 1
        self.final_ratio = self.ratio