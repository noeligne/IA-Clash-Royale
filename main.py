import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from ia_CR import *
from pull_deck import tirage_aleatoire
from cartes import TRANSLATIONS

class MainWindow(QMainWindow):
    def __init__(self, main_prog):
        super().__init__()

        self.main = main_prog
        self.setWindowTitle("Clash AI")
        self.resize(900, 600)

        self.pages = QStackedWidget()

        self.home_page = self.create_home_page()
        self.generator_page = self.deck_generator()

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.generator_page)

        self.setCentralWidget(self.pages)
    
    def create_home_page(self):
        page = QWidget()

        title = QLabel("Clash Royale Deck generator")
        open_button = QPushButton("Open generator")

        open_button.clicked.connect(self.show_generator)
        layout = QVBoxLayout()
        layout.addWidget(title)
        layout.addWidget(open_button)
        page.setLayout(layout)
        return page

    def deck_generator(self):
        page = QWidget()
        self.title_label = QLabel("Deck Generator")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.card_labels = []

        deck_layout = QGridLayout()

        for index in range(8):
            card_label = QLabel(f"Card {index + 1}")
            card_label.setMinimumSize(160, 100)
            card_label.setFrameShape(QFrame.Shape.Box)

            row = index // 4
            column = index % 4

            deck_layout.addWidget(card_label, row, column)
            self.card_labels.append(card_label)
        
        self.generate_button = QPushButton("Generate a deck")
        bdd = load_bdd(self.main.db)
        bdd = sync_preset(self.main, bdd)
        self.main.collection.update(bdd)
        load_synergy(self.main.synergy, self.main.collection)
        self.generate_button.clicked.connect(self.generate_deck)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(deck_layout)
        main_layout.addWidget(self.generate_button)
        page.setLayout(main_layout)
        return page

    def new_preset(self):
        page = QWidget()
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Exemple : Deck principal")
        self.set_avg_elixir()
        self.set_hero_slots()
        self.result_label = QLabel()

        self.create_button = QPushButton("Créer le preset")
        self.create_button.clicked.connect(self.create_preset)

        form_layout = QFormLayout()
        form_layout.addRow("Name :", self.name_input)
        form_layout.addRow("Average elixir :", self.elixir_input)
        form_layout.addRow("Champions number :", self.hero_slots_input)

        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.create_button)
        main_layout.addWidget(self.result_label)
        page.setLayout(main_layout)
        return page

    def set_avg_elixir(self):
        self.elixir_input = QDoubleSpinBox()
        self.elixir_input.setRange(1.0, 7.0)
        self.elixir_input.setValue(3.5)
        self.elixir_input.setSingleStep(0.1)

    def set_hero_slots(self):
        self.hero_slots_input = QSpinBox()
        self.hero_slots_input.setRange(0, 3)
        self.hero_slots_input.setValue(0)
    
    def create_preset(self):
        name = self.name_input.text().strip()
        average_elixir = self.elixir_input.value()
        hero_slots = self.hero_slots_input.value()

        if not name:
            self.result_label.setText("You must set a name for the preset")
            return
        
        message = (
            f"Preset : {name}\n"
            f"Elixir : {average_elixir}\n"
            f"Champions slots : {hero_slots}"
        )
        self.result_label.setText(message)

    def generate_deck(self):
        deck = tirage_aleatoire(self.main.collection, self.main.setting, self.main.synergy)
        for label, card in zip(self.card_labels, deck.deck):
            label.setText(TRANSLATIONS[card.nom])
    
    def show_home_page(self):
        self.pages.setCurrentWidget(self.home_page)
    
    def show_generator(self):
        self.pages.setCurrentWidget(self.generator_page)

def main():
    app = QApplication(sys.argv)
    main_prog = Main()
    main_prog.start()

    window = MainWindow(main_prog)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()