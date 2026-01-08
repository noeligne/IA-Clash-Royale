class Carte:
    def __init__(self, nom, ratio, heros, elixir):
        self.nom = nom
        self.ratio = ratio
        self.heros = heros
        self.elixir = elixir
    
    def ajoutescore(self, score):
        if self.ratio + score >= 1:
            self.ratio += score
        else :
            self.ratio = 1