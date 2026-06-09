import random
from cartes import *
from synergy import *

def tirage_aleatoire(collection, setting, synergies):
    deck = Deck(setting)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        if (deck.is_card_in_deck(carte.nom)):
            synergies.pull_boost(carte)
        pool.remove(carte)
    collection.reset_final_ratio()
    return deck