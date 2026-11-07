
import sys

from PySide6.QtWidgets import *
from PySide6.QtCore import *

from ia_CR import *
from pull_deck import tirage_aleatoire
from cartes import CARDS_STATIC
from synergy import TRIPLETS

# Vérifie que ces deux fonctions sont bien importées
# depuis les fichiers où tu les as définies.
# from triple_draft import triple_draft_mode
# from deck_suggester import suggest_deck


class MainWindow(QMainWindow):

    def __init__(self, main_prog):
        super().__init__()

        # =============================
        # INITIALISATION
        # =============================

        self.main = main_prog

        self.setWindowTitle("Clash AI")
        self.resize(1000, 700)

        self.current_deck = None
        self.current_mode = None

        self.modes = {
            "1": tirage_aleatoire,
            "2": triple_draft_mode_app,
            "3": suggest_deck_app
        }

        # =============================
        # CHARGEMENT DES DONNÉES
        # =============================

        bdd = load_bdd(self.main.db)
        bdd = sync_preset(self.main, bdd)

        self.main.collection.update(bdd)

        load_synergy(
            self.main.synergy,
            self.main.collection
        )

        # =============================
        # CRÉATION DES PAGES
        # =============================

        self.triple_draft_state = None
        self.triple_draft_choices = []

        self.pages = QStackedWidget()

        self.home_page = self.create_home_page()
        self.generator_page = self.create_generator_page()

        self.settings_page = self.create_placeholder_page(
            "Settings",
            "Settings will be available here."
        )

        self.multiple_decks_page = self.create_placeholder_page(
            "Multiple Decks Generator",
            "Generate multiple decks here."
        )

        self.pages.addWidget(self.home_page)
        self.pages.addWidget(self.generator_page)
        self.pages.addWidget(self.settings_page)
        self.pages.addWidget(self.multiple_decks_page)

        self.setCentralWidget(self.pages)

        self.show_home_page()

    # =================================
    # MENU PRINCIPAL
    # =================================

    def create_home_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("CLASH AI")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            margin: 30px;
        """)

        subtitle = QLabel("Choose a mode")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("font-size: 18px;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(20)

        buttons = [
            ("Deck Generator", lambda: self.open_mode("1")),
            ("Triple Draft Mode", lambda: self.open_mode("2")),
            ("Deck Suggester", lambda: self.open_mode("3")),
            ("Settings", self.show_settings),
            ("Multiple Decks Generator", self.show_multiple_decks)
        ]

        positions = [
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 0),
            (1, 1)
        ]

        for (name, callback), (row, col) in zip(buttons, positions):

            button = QPushButton(name)
            button.setMinimumSize(200, 120)

            button.setStyleSheet("""
                QPushButton {
                    background-color: #252a35;
                    color: white;
                    border-radius: 12px;
                    font-size: 17px;
                    font-weight: bold;
                }

                QPushButton:hover {
                    background-color: #394354;
                }
            """)

            button.clicked.connect(callback)

            grid.addWidget(button, row, col)

        layout.addStretch()
        layout.addLayout(grid)
        layout.addStretch()

        return page

    # =================================
    # PAGE DE GÉNÉRATION
    # =================================

    def create_generator_page(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        self.generator_title = QLabel("Deck Generator")
        self.generator_title.setAlignment(Qt.AlignCenter)

        self.generator_title.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            margin: 15px;
        """)

        layout.addWidget(self.generator_title)

        # Affichage des 8 cartes
        cards_layout = QGridLayout()
        cards_layout.setSpacing(15)

        self.card_labels = []

        for i in range(8):

            label = QLabel("Empty")
            label.setAlignment(Qt.AlignCenter)
            label.setMinimumSize(150, 120)

            label.setStyleSheet("""
                QLabel {
                    background-color: #252a35;
                    color: white;
                    border-radius: 10px;
                    font-size: 16px;
                    font-weight: bold;
                }
            """)

            self.card_labels.append(label)

            cards_layout.addWidget(
                label,
                i // 4,
                i % 4
            )

        layout.addLayout(cards_layout)

        # Bouton de génération
        self.generate_button = QPushButton("Generate Deck")
        self.generate_button.setMinimumHeight(45)
        self.generate_button.clicked.connect(self.generate_deck)

        layout.addWidget(self.generate_button)

        # =============================
        # ONGLETS
        # =============================

        self.generator_tabs = QTabWidget()

        self.result_tab = self.create_result_tab()
        self.learning_tab = self.create_learning_tab()
        self.synergy_tab = self.create_synergy_tab()

        self.generator_tabs.addTab(self.result_tab, "Result")
        self.generator_tabs.addTab(self.learning_tab, "Learning")
        self.generator_tabs.addTab(self.synergy_tab, "Synergies")

        layout.addWidget(self.generator_tabs)

        # Retour au menu
        self.back_button = QPushButton("Back to Menu")
        self.back_button.clicked.connect(self.show_home_page)

        layout.addWidget(self.back_button)

        return page

    # =================================
    # ONGLET RESULT
    # =================================

    def create_result_tab(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        layout.addWidget(
            QLabel("How many towers did you destroy?")
        )

        self.win_input = QSpinBox()
        self.win_input.setRange(0, 3)

        layout.addWidget(self.win_input)

        layout.addWidget(
            QLabel("How many of your towers got destroyed?")
        )

        self.loose_input = QSpinBox()
        self.loose_input.setRange(0, 3)

        layout.addWidget(self.loose_input)

        self.confirm_score_button = QPushButton("Confirm Score")
        self.confirm_score_button.clicked.connect(self.submit_result)

        layout.addWidget(self.confirm_score_button)

        return page

    # =================================
    # ONGLET LEARNING
    # =================================

    def create_learning_tab(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        self.score_label = QLabel("Score: -")
        self.average_score_label = QLabel("Average score: -")

        layout.addWidget(self.score_label)
        layout.addWidget(self.average_score_label)

        return page

    # =================================
    # ONGLET SYNERGIES
    # =================================

    def create_synergy_tab(self):

        page = QWidget()
        layout = QVBoxLayout(page)

        self.synergy_info = QLabel("Deck synergies")

        layout.addWidget(self.synergy_info)

        return page

    # =================================
    # OUVERTURE D'UN MODE
    # =================================

    def open_mode(self, mode):

        self.current_mode = mode

        titles = {
            "1": "Deck Generator",
            "2": "Triple Draft Mode",
            "3": "Deck Suggester"
        }

        self.generator_title.setText(titles[mode])

        self.pages.setCurrentWidget(self.generator_page)

        self.generate_deck()

    # =================================
    # GÉNÉRATION DU DECK
    # =================================

    
    def generate_deck(self):

        if self.current_mode not in self.modes:
            return

        # Génération selon le mode choisi
        self.current_deck = self.modes[self.current_mode](
            self.main.collection,
            self.main.setting,
            self.main.synergy
        )

        # Réinitialisation des ratios après le tirage
        self.main.collection.reset_final_ratio()

        # Le Triple Draft a été annulé
        if self.current_deck is None:

            self.generate_button.setEnabled(True)
            self.confirm_score_button.setEnabled(False)

            return

        # Évolution automatique des héros
        auto_evo_hero(self.current_deck)

        # Affichage des huit cartes
        for i, label in enumerate(self.card_labels):

            if i < len(self.current_deck.deck):

                card = self.current_deck.deck[i]

                label.setText(
                    CARDS_STATIC.data[card.nom]["name"][
                        self.main.setting.lang
                    ]
                )

            else:
                label.setText("Empty")

        # Réinitialisation des résultats
        self.win_input.setValue(0)
        self.loose_input.setValue(0)

        self.score_label.setText("Score: -")
        self.average_score_label.setText("Average score: -")

        self.confirm_score_button.setEnabled(True)
        self.generate_button.setEnabled(False)


    # =================================
    # ENREGISTREMENT DU RÉSULTAT
    # =================================

    
    def submit_result(self):

        if self.current_deck is None:
            return

        win = self.win_input.value()
        loose = self.loose_input.value()

        # Calcul du score
        if win - loose < 0:
            score = win - (loose * (1 - 0.1 * win))
        else:
            score = win - loose

        # =============================
        # APPRENTISSAGE
        # =============================

        # Mise à jour des triplets
        TRIPLETS.deck_score(
            self.current_deck,
            score
        )

        # Mise à jour des statistiques des cartes
        self.current_deck.gagne(
            score,
            self.main.collection.avg_score(),
            self.main.setting.m_elixir
        )

        # Mise à jour des synergies
        self.current_deck.update_deck_synergy(
            score,
            self.main.synergy
        )

        # =============================
        # SAUVEGARDE DES DONNÉES
        # =============================

        # Sauvegarde de la base de données des cartes
        save_bdd(
            self.main.collection,
            self.main.db
        )

        # Sauvegarde des synergies
        save_synergy(
            self.main.synergy
        )

        # =============================
        # ACTUALISATION DE L'INTERFACE
        # =============================

        self.score_label.setText(f"Score: {score}")

        self.average_score_label.setText(
            f"Average score: {self.main.collection.avg_score()}"
        )

        # Empêcher une seconde validation
        self.current_deck = None

        self.confirm_score_button.setEnabled(False)
        self.generate_button.setEnabled(True)


        # =================================
        # PAGES SECONDAIRES
        # =================================

    def create_placeholder_page(self, title, description):

        page = QWidget()
        layout = QVBoxLayout(page)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        description_label = QLabel(description)
        description_label.setAlignment(Qt.AlignCenter)

        back_button = QPushButton("Back to Menu")
        back_button.clicked.connect(self.show_home_page)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(back_button)

        return page

    # =================================
    # NAVIGATION
    # =================================

    def show_home_page(self):

        self.pages.setCurrentWidget(self.home_page)

    def show_settings(self):

        self.pages.setCurrentWidget(self.settings_page)

    def show_multiple_decks(self):

        self.pages.setCurrentWidget(self.multiple_decks_page)

if __name__ == "__main__":

    app = QApplication(sys.argv)

    main_prog = Main()  # Ton objet principal existant
    main_prog.start(mode="app")  # Démarre le programme principal

    window = MainWindow(main_prog)
    window.show()

    sys.exit(app.exec())