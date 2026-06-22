class Settings:
    def __init__(self, m_elixir = 3.5):
        self.m_elixir = m_elixir
        self.banlist = list()
        self.main = None
        self.heros = 1
        self.player_tag = ""
        self.player = None
    
    def set_main(self, main, local):
        self.main = main
        if (not local):
            import clash_royale
            from dotenv import load_dotenv
            import os
            load_dotenv()
            API_KEY = os.getenv("API_KEY")
            CLIENT = clash_royale.Client(api_key = API_KEY)

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
        print("\n Settings :\n1 - Average elixir\n2 - Ban a card\n3 - Unban a card\n4 - Change number of Heroes\n5 - Change preset\n6 - Change card level\n7 - Set player id\n8 - Exit (write the number corresponding to the setting you want)")
        menu = {1 : self.change_avg_elixir, 2 : self.exclusion, 3 : self.inclusion, 4 : self.heros_slot, 5 : self.main.load_preset, 6 : self.change_level, 7 : self.set_player, 8 :self.main.main_menu}
        try:
            param = int(input())
            menu[param]()
        except NameError:
            print("Invalid input")
            return
    
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
                    carte.banned = True
                    if (input("Would you like to ban another card ? (y/n)\n") == "y"):
                        return self.exclusion()
                    self.modified_set()
                    return
            if (input("I did not find the card you searched for, do you want to exit ? (y/n)\n") == "n"):
                return self.exclusion()
        else :
            for ban in start:
                for carte in self.main.collection.collection:
                    if carte.nom == ban:
                        self.banlist.append(carte)
                        carte.banned = True
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
                self.banlist[carte].banned = False
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
    
    def change_level(self):
        for carte in self.main.collection.collection:
            if carte not in self.banlist:
                print(f"{carte.nom} : lvl {carte.level}")
        change = input("Which card do you what to edit ?\n")
        for carte in self.main.collection.collection:
            if carte.nom == change:
                try :
                    carte.level = int(input("Which level do you want to set for this card ?\n"))
                    print(f"{carte.nom} level successfully set to {carte.level}")
                    if (input("Would you like to change another card ? (y/n)\n") == "y"):
                        return self.change_level()
                    return
                except:
                    if (input("The input is incorrect, do you want to exit ?\n") == "n"):
                        return self.change_level()
        if (input("I did not find the card you searched for, do you want to exit ? (y/n)\n") == "n"):
            return self.change_level()
    
    def set_player(self, start = False, tag = None):
        if (self.main.local):
            return
        if (start == True):
            self.player_tag = tag
        else:
            self.player_tag = input("Enter your tag here: ")
        try:
            self.player = client.players.get(self.player_tag)
            print("Welcome", self.player.name, "\n")
        except clash_royale.ClashRoyaleNotFoundError:
            print("Player not found")
        except clash_royale.UnauthorizedError:
            print("Invalid API key")
        except clash_royale.RateLimitError:
            print("Rate limit exceeded")
        except clash_royale.ClashRoyaleHTTPError as e:
            print(f"API error: {e}")

    def modified_set(self):
        s = input("Do you want to save the modified preset ? (y/n)\n")
        if (s == "y"):
            self.main.save_preset()