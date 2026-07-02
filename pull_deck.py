import random
from cartes import *
from synergy import *

def boost_elixir(deck, setting, collection):
    total = deck.elixir_sum()
    total_goal = setting.m_elixir * 8
    nb_cards = len(deck.deck)
    left = total_goal - total
    remaining = (8 - nb_cards)
    if remaining == 0:
        return
    avg_left = left / remaining
    if avg_left <= 0:
        goal = 1
    else:
        goal = avg_left
    if nb_cards == 0:
        return
    for carte in collection.collection:
        ecart = abs(goal - carte.elixir)
        carte.final_ratio *= 1 + (((nb_cards + 1) / 8) * (2 / (ecart + 1) - 1))

def tirage_aleatoire(collection, setting, synergies):
    deck = Deck(setting)
    pool = collection.collection[:]
    while not deck.plein():
        carte = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        if (deck.is_card_in_deck(carte.nom)):
            synergies.pull_boost(carte)
            boost_elixir(deck, setting, collection)
        pool.remove(carte)
    collection.reset_final_ratio()
    return deck