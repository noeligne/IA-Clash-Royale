import random
from cartes import *
from synergy import *

def boost_elixir(deck, setting, collection):
    elixir_dict = {}
    total = deck.elixir_sum()
    total_goal = setting.m_elixir * 8
    nb_cards = len(deck.deck)
    left = total_goal - total
    accuracy = 0.5
    remaining = (8 - nb_cards)
    if remaining == 0:
        return {}
    avg_left = left / remaining
    if avg_left <= 0:
        goal = 1
    else:
        goal = avg_left
    if nb_cards == 0:
        return {}
    for carte in collection.collection:
        ecart = abs(goal - carte.elixir)
        elixir_dict[carte.nom] = max(0.1, 1 + (1 + accuracy) * (((nb_cards + 2) / 8) * (2 / (ecart + 1 + accuracy) - 1)))
    return elixir_dict

def apply_elixir_boost(collection, elixir_dict):
    if not elixir_dict == {}:
        for carte in collection.collection:
            carte.final_ratio *= elixir_dict[carte.nom]
    return

def delete_elixir_boost(collection, elixir_dict):
    if not elixir_dict == {}:
        for carte in collection.collection:
            carte.final_ratio = carte.final_ratio / elixir_dict[carte.nom]
    return

def tirage_aleatoire(collection, setting, synergies):
    deck = Deck(setting)
    pool = collection.collection[:]
    elixir_dict = {}
    triplet_list = set()
    while not deck.plein():
        carte = random.choices(pool, weights = [c.final_ratio for c in pool], k=1)[0]
        deck.ajoute_carte(carte)
        if (deck.is_card_in_deck(carte.nom)):
            synergies.pull_boost(carte)
            triplet_list = TRIPLETS.boost_triplets(deck, collection, triplet_list)
            delete_elixir_boost(collection, elixir_dict)
            elixir_dict = boost_elixir(deck, setting, collection)
            apply_elixir_boost(collection, elixir_dict)
        pool.remove(carte)
    #collection.reset_final_ratio()
    return deck

def triple_draft_mode(collection, setting, synergies):
    deck = Deck(setting)
    pool = collection.collection[:]
    elixir_dict = {}
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
            delete_elixir_boost(collection, elixir_dict)
            elixir_dict = boost_elixir(deck, setting, collection)
            apply_elixir_boost(collection, elixir_dict)
        for card in d.keys():
            if deck.can_be_added(d[card]) and d[card] not in deck.deck:
                pool.append(d[card])
    print("Here is your deck:")
    #collection.reset_final_ratio()
    return deck

def auto_evo_hero(deck):
    if not CARDS_STATIC.data[deck.deck[0].nom]["evolution"]:
        for i in range(1, len(deck.deck), 1):
            if CARDS_STATIC.data[deck.deck[i].nom]["evolution"]:
                deck.swap(0, i)
                break
    for i in range(len(deck.deck)):
        if CARDS_STATIC.data[deck.deck[i].nom]["champion"] and i not in (1, 2):
            if not CARDS_STATIC.data[deck.deck[1].nom]["champion"]:
                deck.swap(1, i)
            elif not CARDS_STATIC.data[deck.deck[2].nom]["champion"]:
                deck.swap(2, i)
    if not CARDS_STATIC.data[deck.deck[1].nom]["heros"] and not CARDS_STATIC.data[deck.deck[1].nom]["champion"]:
        for i in range(2, len(deck.deck)):
            if CARDS_STATIC.data[deck.deck[i].nom]["heros"] or CARDS_STATIC.data[deck.deck[i].nom]["champion"]:
                deck.swap(1, i)
                break
    if not CARDS_STATIC.data[deck.deck[2].nom]["heros"] and not CARDS_STATIC.data[deck.deck[2].nom]["evolution"] and not CARDS_STATIC.data[deck.deck[2].nom]["champion"]:
            for i in range(3, len(deck.deck), 1):
                if CARDS_STATIC.data[deck.deck[i].nom]["heros"] or CARDS_STATIC.data[deck.deck[i].nom]["evolution"] or CARDS_STATIC.data[deck.deck[i].nom]["champion"]:
                    deck.swap(2, i)
                    break