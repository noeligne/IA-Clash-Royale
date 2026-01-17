class Settings:
    def __init__(self, m_elixir = 3.5):
        self.m_elixir = m_elixir
        self.banlist = list()
        self.main = None
        self.heros = 1
    
    def set_main(self, main):
        self.main = main
    
    def change_avg_elixir(self, start = False):
        try :
            print(f"\nvers quelle valeur voulez vous que la moyenne du coût d'elixir tende ? \n(de base = 3.5, actuelle: {self.m_elixir})")
            m_elixir = float(input())
        except :
            return self.change_avg_elixir(start)
        if m_elixir < 0:
            m_elixir = -m_elixir
        if m_elixir > 7.1:
            m_elixir = 7.1
        print(f"La moyenne tendra donc vers: {m_elixir}\n")
        self.m_elixir = m_elixir
        if not start :
            self.modified_set()
    
    def settings(self):
        print("\n Menu des paramètres :\n1 - Moyenne elixir\n2 - Exclure une carte\n3 - Réinclure une carte\n4 - Nombre de cases héros\n5 - Change preset\n6 - Exit(sélectionnez le numéro correspondant au paramètre désiré)")
        menu = {1 : self.change_avg_elixir, 2 : self.exclusion, 3 : self.inclusion, 4 : self.heros_slot, 5 : self.main.load_preset, 6 : self.main.main_menu}
        try:
            param = int(input())
            menu[param]()
        except:
            print("Invalid input")
            return self.settings()
    
    def exclusion(self, start = False):
        if not start:
            print("choisis la carte à bannir :")
            for carte in self.main.collection.collection:
                if carte not in self.banlist:
                    print(carte.nom)
            ban = input()
            for carte in self.main.collection.collection:
                if carte.nom == ban:
                    self.banlist.append(carte)
                    if (input("Would you like to ban another card ? (y/n)\n") == "y"):
                        return self.exclusion()
                    self.modified_set()
                    return
            if (input("I did not find the card you searched for, do you want to exit ? (y/n)\n") == "n"):
                return self.exclusion()
        else :
            for ban in start:
                print(ban)
                for carte in self.main.collection.collection:
                    if carte.nom == ban:
                        self.banlist.append(carte)
                        print(f"\"{carte.nom}\" card successfully banned")
            print()
            return
    
    def inclusion(self):
        if self.banlist == []:
            print("You don't have any banned cards")
            return
        for carte in self.banlist:
            print(carte.nom)
        unban = input("Which card do you want to unban ?\n")
        for carte in range(len(self.banlist)):
            if unban == self.banlist[carte].nom:
                del(self.banlist[carte])
                print(f"{unban} Successfully unbanned")
                self.modified_set()
                return

    def get_banned_cars_str(self):
        string = ""
        for card in range(len(self.banlist)):
            if card != len(self.banlist) + 1:
                string += str(self.banlist[card].nom) + ";"
            else :
                string += str(self.banlist[card].nom)
        print(string)
        return string
    
    def heros_slot(self, start = False):
        try :
            self.heros = int(input(f"How much Hero slot do you have ? (currently: {self.heros})\n"))
        except :
            self.heros_slot(start)
        if self.heros > 2 :
            self.heros = 2
        if self.heros < 0:
            self.heros = 0
        if not start :
            self.modified_set()
    
    def modified_set(self):
        s = input("Do you want to save the modified preset ? (y/n)\n")
        if (s == "y"):
            self.main.save_preset()
