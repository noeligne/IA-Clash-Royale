from cartes import *

class Synergies:
    def __init__(self):
        self.synergies = []
    
    def add_synergy(self, first, second, win, lose):
        for syn in self.synergies:
            if (syn.is_card_in(first) and syn.is_card_in(second)):
                return
        self.synergies.append(Synergy(first, second, win, lose))
    
    def update_synergy(self, first, second, score):
        for syn in self.synergies:
            if (syn.is_card_in(first) and syn.is_card_in(second)):
                if (score < 0):
                    syn.lose += 1
                elif (score > 0):
                    syn.win += 1
                return
        if (score < 0):
            self.add_synergy(first, second, 0, 1)
        elif (score > 0):
            self.add_synergy(first, second, 1, 0)
        else:
            self.add_synergy(first, second, 0, 0)
    
    def pull_boost(self, card):
        for syn in self.synergies:
            if (syn.is_card_in(card)):
                if (syn.first.nom == card.nom):
                    syn.second.final_ratio = syn.second.final_ratio * (1 + syn.get_bonus())
                else:
                    syn.first.final_ratio = syn.first.final_ratio * (1 + syn.get_bonus())

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