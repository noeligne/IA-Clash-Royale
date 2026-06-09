from cartes import *

class Synergies:
    def __init__(self):
        self.synergies = []
    
    def add_synergy(self, first, second, win, lose):
        for syn in self.synergies:
            if (syn.is_card_in(first) and syn.is_card_in(second)):
                return
        self.synergies.append(Synergy(first, second, win, lose))

class Synergy:
    def __init__(self, first_card, second_card, win, lose):
        self.first = first_card
        self.second = second_card
        self.win = win
        self.lose = lose

    def get_bonus(self):
        if (self.win == 0 and self.lose == 0):
            return 0
        return (self.win - (self.lose / 2)) / (self.win + self.lose)
    
    def is_card_in(self, card):
        if (card.nom == self.first.nom or card.nom == self.second.nom):
            return True
        return False