import random
from cartes import *

def tirage_aleatoire(collection, setting):
    deck = Deck(setting)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        pool.remove(carte)
    return deck