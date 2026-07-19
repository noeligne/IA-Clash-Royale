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

def triple_draft_mode(collection, setting, synergies):
    deck = Deck(setting)
    pool = collection.collection[:]
    while not deck.plein():
        card1 = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        pool.remove(card1)
        card2 = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        pool.remove(card2)
        card3 = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        pool.remove(card3)
        d = {"1" : card1, "2" : card2, "3" : card3}
        if deck.can_be_added(card1) and deck.can_be_added(card2) and deck.can_be_added(card3):
            choice = ""
            while choice not in d.keys():
                print(f"\nChoose which card do you want to take:\n1 - {card1.nom}: lvl{card1.level}\n2 - {card2.nom}: lvl{card2.level}\n3 - {card3.nom}: lvl{card3.level}\n")
                choice = input("Enter the number associated with the card: ")
            carte = d[choice]
            deck.ajoute_carte(carte)
            print(f"You took {carte.nom} ! That's an excellent choice !\n")
            if not deck.plein():
                deck.affiche()
            synergies.pull_boost(carte)
            boost_elixir(deck, setting, collection)
        for card in d.keys():
            if deck.can_be_added(d[card]) and d[card] not in deck.deck:
                pool.append(d[card])
    print("Here is your deck:")
    collection.reset_final_ratio()
    return deck