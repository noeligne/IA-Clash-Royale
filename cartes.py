class Carte:
    def __init__(self, nom, ratio, heros, elixir, level=16):
        self.nom = nom
        self.ratio = ratio
        self.heros = heros
        self.elixir = elixir
        self.banned = False
        self.level = level
    
    def ajoutescore(self, score):
        if self.ratio + score >= 1:
            self.ratio += score
        else :
            self.ratio = 1