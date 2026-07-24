TRANSLATIONS = {"archer magique" : "Magic Archer",
                "archeres" : "Archers",
                "arc-x" : "X-Bow",
                "armee de squelettes" : "Skeleton Army",
                "artificiere" : "Firecracker",
                "ballon" : "Balloon",
                "barbares d'elite" : "Elite Barbarians",
                "barbares" : "Barbarians",
                "bebe dragon" : "Baby Dragon",
                "belier de combat" : "Battle Ram",
                "berserker" : "Berserker",
                "bombardier" : "Bomber",
                "boule de feu" : "Fireball",
                "boule de neige" : "Giant Snowball",
                "bouliste" : "Bowler",
                "bourreau" : "Executioner",
                "buche" : "The Log",
                "bucheron" : "Lumberjack",
                "buisson suspicieux" : "Suspicious Bush",
                "cabane de barbares" : "Barbarian Hut",
                "cabane de gobelin" : "Goblin Hut",
                "cage gobeline" : "Goblin Cage",
                "canon" : "Cannon",
                "cavabeliere" : "Ram Rider",
                "charrette a canon" : "Cannon Cart",
                "chasseur" : "Hunter",
                "chauves-souris" : "Bats",
                "cheffe des voleuses" : "Boss Bandit",
                "chevalier d'or" : "Golden Knight",
                "chevalier" : "Knight",
                "chevaucheur de cochon" : "Hog Rider",
                "cimetiere" : "Graveyard",
                "clonage" : "Clone Spell",
                "cochon royaux" : "Royal Hogs",
                "colis royal" : "Royal Delivery",
                "dragon de l'enfer" : "Inferno Dragon",
                "dragon squelettes" : "Squeleton Dragons",
                "electrocuteur" : "Zappies",
                "electrocution" : "Zap",
                "electro-dragon" : "Electro Dragon",
                "electro-esprit" : "Electro Spirit",
                "electro-geant" : "Electro Giant",
                "electro-sorcier" : "Electro Wizard",
                "esprit de feu" : "Fire Spirit",
                "esprit de glace" : "Ice Spirit",
                "esprit de guerison" : "Heal Spirit",
                "extracteur d elixir" : "Elixir Collector",
                "fantome royal" : "Royal Ghost",
                "fleche" : "Arrows",
                "foreuse gobeline" : "Goblin Drill",
                "foudre" : "Lightning",
                "fournaise" : "Furnace",
                "fripons" : "Rascals",
                "fut a barbare" : "Barbarian Barrel",
                "fut a gobelin" : "Goblin Barrel",
                "fut a squelettes" : "Squeleton Barrel",
                "gang de gobelin" : "Goblin Gang",
                "gardes" : "Guards",
                "gargouille" : "Minions",
                "geant royal" : "Royal Giant",
                "geant" : "Giant",
                "geante runique" : "Rune Giant",
                "gel" : "Freeze",
                "gobelin a lance" : "Spear Goblin",
                "gobelin a sarbacane" : "Dart Goblin",
                "gobelin explosif" : "Goblin Demolisher",
                "gobelin geant" : "Goblin Giant",
                "gobelins" : "Goblins",
                "gobelinstein" : "Goblinstein",
                "golem de glace" : "Ice Golem",
                "golem d'elixir" : "Elixir Golem",
                "golem" : "Golem",
                "guerrisseuse armee" : "Battle Healer",
                "horde de gargouille" : "Minion Horde",
                "imperatrice spirituelle" : "Spirit Empress",
                "machine gobeline" : "Goblin Machine",
                "machine volante" : "Flying Machine",
                "maitre mineur" : "Mighty Miner",
                "malediction gobeline" : "Goblin Curse",
                "mamie sorciere" : "Mother Witch",
                "mega chevalier" : "Mega Knight",
                "mega gargouille" : "Mega Minion",
                "mineur" : "Miner",
                "mini p.e.k.k.a" : "Mini P.E.K.K.A",
                "miroir" : "Mirror",
                "moine" : "Monk",
                "molosse de lave" : "Lava Hound",
                "mortier" : "Mortar",
                "mousquetaire" : "Musketeer",
                "neant" : "Void",
                "p.e.k.k.a" : "P.E.K.K.A",
                "pecheur" : "Fisherman",
                "petit prince" : "Little Prince",
                "phenix" : "Phoenix",
                "pierre tombale" : "Tombstone",
                "poison" : "Poison",
                "prince tenebreux" : "Dark Prince",
                "prince" : "Prince",
                "princesse" : "Princess",
                "rage" : "Rage",
                "recrues royales" : "Royal Recruits",
                "reine des archers" : "Archer Queen",
                "roi squelette" : "Skeleton King",
                "ronces" : "Vines",
                "ronin" : "Ronin",
                "roquette" : "Rocket",
                "sapeurs" : "Wall Breakers",
                "seisme" : "Earthquake",
                "sorcier de glace" : "Ice Wizard",
                "sorcier" : "Wizard",
                "sorciere de la nuit" : "Night Witch",
                "sorciere" : "Witch",
                "squelette geant" : "Giant Squeleton",
                "squelettes" : "Skeletons",
                "tesla" : "Tesla",
                "tornade" : "Tornado",
                "tour a bombe" : "Bomb Tower",
                "tour de l'enfer" : "Inferno Tower",
                "trois mousquettaires" : "Three Musketeers",
                "valkyrie" : "Valkyrie",
                "voleuse" : "Bandit",
                "zappy" : "Sparky"}

class Deck:
    def __init__(self, setting):
        self.deck = []
        self.banlist= setting.banlist
        self.maxi = 0
        self.heros = 0
        self.setting = setting
    
    def plein(self):
        return len(self.deck) == 8
    
    def can_be_added(self, carte):
        if self.plein():
            return False
        if carte.heros:
            if self.heros == self.setting.heros:
                return False
        if carte in self.deck:
            return False
        if carte in self.banlist:
            return False
        return True

    def ajoute_carte(self, carte):
        if not self.can_be_added(carte):
            return
        if carte.heros:
            self.heros += 1
        self.deck.append(carte)
    
    def vide_deck(self):
        self.deck = []
        self.heros = 0
    
    def gagne(self, score, avg_score, m_elixir):
        coeff = score
        for carte in self.deck:
            if score > 0 :
                ratio_percentage = (1 + ((avg_score - carte.ratio) / avg_score))
                if ratio_percentage <= 0:
                    ratio_percentage = 0.01
                coeff = score * ratio_percentage * 1.2 * (carte.level / 16)
            else :
                coeff = score * (1 + ((carte.ratio - avg_score) / avg_score)) * 0.75 * (carte.level / 16)
            carte.ajoutescore(coeff)

    def plus_caractere(self):
        if len(self.deck) == 0:
            return 0
        maxi = len(self.deck[0].nom)
        for carte in self.deck:
            if len(carte.nom) > maxi:
                maxi = len(carte.nom)
        self.maxi = maxi
    
    def affiche(self):
        string = ""
        index = 0
        separator = ["/", "|", "|", "|", "\\\n\\", "|", "|", "|", "/"]
        self.plus_caractere()
        if self.plein():
            for i in range(8):
                string += separator[i]
                middle = round((self.maxi + 2 - len(TRANSLATIONS[self.deck[index].nom]))/2)
                if len(TRANSLATIONS[self.deck[index].nom]) < self.maxi :
                    if (self.maxi - len(TRANSLATIONS[self.deck[index].nom])) % 2 == 0:
                        string += " " * middle + str(TRANSLATIONS[self.deck[index].nom]) + " " * middle
                    elif middle > (self.maxi + 2 - len(TRANSLATIONS[self.deck[index].nom]))/2 :
                        string += " " * (middle - 1) + str(TRANSLATIONS[self.deck[index].nom]) + " " * middle
                    else :
                        string += " " * middle + str(TRANSLATIONS[self.deck[index].nom]) + " " * (middle + 1)
                else :
                    string += " " + str(TRANSLATIONS[self.deck[index].nom]) + " "
                index += 1
            string += separator[i + 1] + "\n"
            print(string)
        else :
            print("So far your team is composed of :")
            for card in self.deck:
                print(f"- {TRANSLATIONS[card.nom]}")
            print()

    def avg_elixir(self):
        nb = 0
        elixir = 0
        for carte in self.deck :
            elixir += carte.elixir
            nb += 1
        if nb > 0:
            return elixir / nb
        else:
            return 0
    
    def elixir_sum(self):
        elixir = 0
        for carte in self.deck:
            elixir += carte.elixir
        return elixir
    
    def is_card_in_deck(self, nom):
        for carte in self.deck:
            if (carte.nom == nom):
                return True
        return False

    def update_deck_synergy(self, score, synergies):
        for i in range(len(self.deck)):
            for j in range(i + 1, len(self.deck), 1):
                synergies.update_synergy(self.deck[i], self.deck[j], score)

class Carte:
    def __init__(self, nom, ratio, heros, elixir, level=16):
        self.nom = nom
        self.ratio = ratio
        self.final_ratio = ratio
        self.heros = heros
        self.elixir = elixir
        self.banned = False
        self.level = level
    
    def ajoutescore(self, score):
        if self.ratio + score >= 1:
            self.ratio += score
        else :
            self.ratio = 1
        self.final_ratio = self.ratio