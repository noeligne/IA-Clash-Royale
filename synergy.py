from cartes import *
from config import Config
import math

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
        total = self.win + self.lose
        defeat_factor = max(0.6, min(0.95, (total) / 20))
        bonus = (self.win - (self.lose * defeat_factor)) / (total) * math.log(total + 1)
        return max(-0.9, min(2, bonus))
    
    def is_card_in(self, card):
        if (card.nom == self.first.nom or card.nom == self.second.nom):
            return True
        return False

class Triplet:
    def __init__(self):
        self.data = Config("./global/triplet.json")

    def get_key(self, card1, card2, card3):
        key = "|".join(sorted([card1.nom, card2.nom, card3.nom]))
        return key

    def update_triplet(self, card1, card2, card3, score):
        if score == 0:
            return
        key = self.get_key(card1, card2, card3)
        if key not in self.data.data.keys():
            self.data.data[key] = {"cards" : [card1.nom, card2.nom, card3.nom], 
                              "wins" : 0, "losses" : 0, "total" : 0}
        if score > 0:
            self.data.data[key]["wins"] += 1
        elif score < 0:
            self.data.data[key]["losses"] += 1
        self.data.data[key]["total"] += 1

    def deck_score(self, deck, score):
        length = len(deck.deck)
        for card1 in range(length):
            for card2 in range(card1 + 1, length, 1):
                for card3 in range(card2 + 1, length, 1):
                    self.update_triplet(deck.deck[card1], deck.deck[card2], deck.deck[card3], score)
        self.data.save()

    def get_bonus(self, card1, card2, card3):
        key = self.get_key(card1, card2, card3)
        if key not in self.data.data.keys():
            return 0
        total = self.data.data[key]["total"]
        win = self.data.data[key]["wins"]
        loss = self.data.data[key]["losses"]
        defeat_factor = max(0.6, min(0.95, (total) / 20))
        bonus = (win - (loss * defeat_factor)) / (total) * math.log(total + 1)
        final_bonus = bonus * 0.15
        return max(-0.45, min(0.25, final_bonus))
        

    def boost_triplets(self, deck, collection, boosted = None):
        length = len(deck.deck)
        if boosted == None:
            boosted = set()
        if length < 2:
            return boosted
        for card1 in range(length):
            for card2 in range(card1 + 1, length, 1):
                for card in collection.collection:
                    if card in deck.deck:
                        continue
                    key = tuple(sorted([deck.deck[card1].nom, deck.deck[card2].nom, card.nom]))
                    if key not in boosted:
                        card.final_ratio *= 1 + self.get_bonus(deck.deck[card1], deck.deck[card2], card)
                        boosted.add(key)
        return boosted

TRIPLETS = Triplet()