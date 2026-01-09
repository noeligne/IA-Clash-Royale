class Settings:
    def __init__(self, m_elixir = 3.5):
        self.m_elixir = m_elixir
        self.banlist = list()
        self.main = None
        self.heros = 1
    
    def set_main(self, main):
        self.main = main
    
    def change_avg_elixir(self):
        try :
            print(f"\nvers quelle valeur voulez vous que la moyenne du coût d'elixir tende ? \n(de base = 3.5, actuelle: {self.m_elixir})")
            m_elixir = float(input())
        except :
            return self.change_avg_elixir()
        if m_elixir < 0:
            m_elixir = -m_elixir
        if m_elixir > 7.1:
            m_elixir = 7.1
        print(f"La moyenne tendra donc vers: {m_elixir}\n")
        self.m_elixir = m_elixir
        self.modified_set()
    
    def settings(self):
        print("\n Menu des paramètres :\n1 - Moyenne elixir\n2 - Exclure une carte\n3 - Nombre de cases héros\n4 - Change preset\n5 - Exit(sélectionnez le numéro correspondant au paramètre désiré)")
        menu = {1 : self.change_avg_elixir, 2 : self.exclusion, 3 : self.heros_slot, 4 : self.main.load_preset, 5 : self.main.main_menu}
        try:
            param = int(input())
            menu[param]()
        except:
            print("Invalid input")
            return self.settings()
    
    def exclusion(self):
        print("choisis la carte à bannir :")
        for carte in self.main.collection.collection:
            if carte not in self.banlist:
                print(carte.nom)
        ban = input()
        for carte in self.main.collection.collection:
            if carte.nom == ban:
                self.banlist.append(carte)
                return
    
    def heros_slot(self):
        try :
            self.heros = int(input(f"How much Hero slot do you have ? (currently: {self.heros})\n"))
        except :
            print("\nInvalid input")
        if self.heros > 2 :
            self.heros = 2
        if self.heros < 0:
            self.heros = 0
        self.modified_set()
    
    def modified_set(self):
        s = input("Do you want to save the modified preset ? (y/n)\n")
        if (s == "y"):
            self.main.save_preset()
