from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QGridLayout,
                             QApplication, QFrame, QComboBox, QVBoxLayout,
                             QLabel, QPushButton, QListWidget, QDialog,
                             QCheckBox, QLineEdit, QWidget)
                             
import sys
import os, webbrowser
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath('../simulateur'))
sys.path.insert(0, os.path.abspath('simulateur/'))

from page_accueil import *
from Interface_saisie import *


from derouleur import deroul,Machine
import gestion_fichiers

class FenetrePrincipale(QMainWindow):
    """
    Fenêtre principale de l'application, contient
    un menu, et la page en train d'être affiché.
    Le menu permet de charger, créer, ou sauvegarder une machine.
    Contient les fenêtres de dialogue gérant ces actions.
    """

    def __init__(self):
        super().__init__()
        self.cree_actions()
        self.setupUI()

    def setupUI(self):
        self.cadre_central = Accueil(self)
        self.setCentralWidget(self.cadre_central)
        self.cree_menus()
        self.setWindowTitle('Simulateur de Machines de Turing')
        self.setGeometry(100, 200, 300, 450)
        self.setWindowIcon(QIcon("gui/Icon/image_appli.png"))
        self.show()

    def cree_actions(self):
        """
        Création des action du menu dans la barre de menu
        """
        #action de creer une machine
        self.creer_machine_act = QAction('&Créer une machine', self)
        self.creer_machine_act.triggered \
                              .connect(self.dialogue_creer_machine)
                              
        #Action de charger une machine depuis un fichier
        self.ouvrir_fichier_act = QAction('Charger une machine', self)
        self.ouvrir_fichier_act.triggered \
                               .connect(self.dialogue_charger_fichier)

        #Action de sauvegarder une machine dans un fichier
        self.sauver_fichier_act = QAction("Sauvegarder la machine", self)
        self.sauver_fichier_act.triggered.connect(self.dialogue_sauver_fichier)

        #Action de quitter l'application
        self.quitter_act = QAction('&Quitter', self)
        self.quitter_act.triggered.connect(app.quit)

        #Action qui ouvre l'aide
        self.aide_act = QAction('&Aide', self)
        self.aide_act.triggered.connect(self.affiche_aide)


    def affiche_aide(self):
        """
        Fonction qui ouvre l'aide.
        Utilise la fonction d'aide de la gestion de fichiers.
        """
        webbrowser.open("gui/aide.html")

    def cree_menus(self):
        """
        Création de la barre de menu
        """
        barre_de_menu = self.menuBar()
        barre_de_menu.setNativeMenuBar(False)
        menu_fichiers = barre_de_menu.addMenu('Fichiers')
        barre_de_menu.addAction(self.aide_act)
        menu_fichiers.addAction(self.creer_machine_act)
        menu_fichiers.addAction(self.ouvrir_fichier_act)
        menu_fichiers.addAction(self.sauver_fichier_act)
        menu_fichiers.addAction(self.quitter_act)

    def changer_page(self, page: QFrame):
        """
        affiche la page 'page' dans la fenêtre
        """
        self.cadre_central.deleteLater()
        self.cadre_central = page(self)
        self.setCentralWidget(self.cadre_central)
        self.cadre_central.show()

    def dialogue_creer_machine(self):
        """
        Permet de créer la fenêtre de dialogue demandant le
        nombre et le type de Ruban
        """
        DialogueCreation(self)

    def dialogue_sauver_fichier(self):
        """
        Création d'un dialogue pour sauvegarder un fichier en
        appelant la méthode de la gestion de fichier
        'écriture_fichier_machine'
        Utilise le Widget QFileDialog
        """
        chemin = QFileDialog.getSaveFileName(self, 'Open file', 'sauvegarde')
        if chemin[0]:
            contenu = Derouleur.machine_courante
            gestion_fichiers.ecriture_fichier_machine(deroul.Derouleur.nb_rubans, contenu, chemin[0])


    def dialogue_charger_fichier(self):
        """
        Création d'un dialogue pour charger un fichier en appelant
        la méthode de la gestion de fichier 'lecture_fichier_machine'

        Utilise le Widget QFileDialog

        Appelle la fonction de réinitialisation du module dérouleur.
        Appelle la fonction lecture d'un fichier, et initialise une nouvelle machine.
        """
        if(Derouleur.machine_courante):
            Derouleur.machine_courante = None
            Derouleur.rubans = []
            
        chemin = QFileDialog.getOpenFileName(self, 'Open file', 'chargement',
                                             "fichiers textes (*.txt *.py)")
        if chemin[0]:
            gestion_fichiers.lecture_fichier_machine(chemin[0])
            self.changer_page(Saisie)
            
    def quitter_appli(self):
         app.quit()

class DialogueCreation(QDialog):
    """
    Le fenêtre de dialogue pour la sélection du nombre
    de rubans et leur type. Amène à la page de saisie
    des règles.
    Assez complexe pour mériter sa propre classe.
    """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUI(parent)
        self.show()

    def setupUI(self, parent):
		
        self.setWindowTitle('nombre de rubans')
		
        self.layout = QGridLayout()
        self.saisie_nbr_ruban = QComboBox(self)
        for i in range(1, 10):
            self.saisie_nbr_ruban.addItem(str(i))

        self.saisie_type_ruban = QCheckBox("Ruban fini à gauche:")
        self.saisie_type_ruban.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.btn_validation = QPushButton("Valider", self)
        self.btn_validation.clicked \
                           .connect(lambda: self.validation_creation(parent))
        self.layout.addWidget(QLabel("Configuration des rubans:", self),
                              0, 0, 1, 3)
        self.layout.addWidget(QLabel("Nombre de rubans:", self), 3, 0, 1, 2)
        self.layout.addWidget(self.saisie_nbr_ruban, 3, 2)
        self.layout.addWidget(self.saisie_type_ruban, 4, 0, 1, 2)
        self.layout.addWidget(self.btn_validation, 5, 0, 1, 2)
        self.setLayout(self.layout)

    def validation_creation(self, parent):
        """
        Appelé lorsque la création est validé par l'utilisateur.
        Transmet le nombre de Ruban au dérouleur.
        Appelle la fonction de réinitialisation du module dérouleur.
        Amène à la création du nombre de Ruban correspondant
        avec le bon type dans le dérouleur.

        Change la page pour passer à la page de Saisie de la
        machine.
        """
        if(Derouleur.machine_courante):
            Derouleur.machine_courante = None
            Derouleur.rubans = []
        Derouleur.nb_rubans = int(self.saisie_nbr_ruban.currentText())
        if self.saisie_type_ruban.isChecked():
            Saisie.types_rub = 1
        else: 
            Saisie.types_rub = 0
        parent.changer_page(Saisie)
        self.hide()
        self.deleteLater()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	fenetre = FenetrePrincipale()
	sys.exit(app.exec_())
