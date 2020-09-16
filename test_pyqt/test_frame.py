from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QGridLayout,
                             QApplication, QFrame, QComboBox, QVBoxLayout,
                             QLabel, QPushButton, QListWidget, QDialog,
                             QCheckBox, QLineEdit, QWidget)
from PyQt5 import QtCore
import gestion_fichiers
import derouleur
import sys


def rien(truc):
    pass


class PageAccueil(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI(parent)

    def setupUI(self, parent):
        self.setStyleSheet('background: rgb(105,150,156)')
        self.btn_nv_machine = QPushButton("Créer une nouvelle machine", self)
        self.btn_nv_machine.clicked.connect(parent.dialogue_creer_machine)
        self.btn_charger_machine = QPushButton("Charger une machine", self)
        self.btn_charger_machine.clicked \
                                .connect(parent.dialogue_charger_fichier)
        self.btn_quitter = QPushButton("Quitter", self)
        self.btn_quitter.clicked.connect(app.quit)
        layout = QVBoxLayout()
        layout.addWidget(self.btn_nv_machine)
        layout.addWidget(self.btn_charger_machine)
        layout.addWidget(self.btn_quitter)
        self.setLayout(layout)


class PageSaisie(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet('background: rgb(235,225,190)')
        btn_lancer = QPushButton("Lancer", self)
        btn_lancer.clicked.connect(lambda: parent.changer_page(PageSimulation))
        layout = QVBoxLayout()
        layout.addWidget(QLabel(str(derouleur.nbr_ruban), self))
        layout.addWidget(btn_lancer)
        self.setLayout(layout)
        # self.lay = QVBoxLayout(self)
        # self.lay.addWidget(self.cb)
        # self.setLayout(self.lay)


class ZoneRuban(QWidget):

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.aff = QLineEdit()
        self.aff.setStyleSheet('background: rgb(250,252,255)')
        layout = QVBoxLayout()
        layout.addWidget(self.aff)
        self.setLayout(layout)


class PageSimulation(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI(parent)

    def setupUI(self, parent):
        self.setStyleSheet('background: rgb(228,152,175)')
        layout = QGridLayout()
        self.setLayout(layout)

        self.affichage_ruban = ZoneRuban()
        layout.addWidget(self.affichage_ruban, 0, 0, 1, 5)
        self.liste_regles = QListWidget()
        self.liste_regles.addItem(" ")
        layout.addWidget(self.liste_regles, 0, 6, 6, 3)

        self.btn_avancer = QPushButton(">", self)
        self.btn_reculer = QPushButton("<", self)
        self.btn_derouler_stop = QPushButton("|>", self)
        self.btn_aller_debut = QPushButton("<<<", self)
        self.btn_aller_fin = QPushButton(">>>", self)
        layout.addWidget(self.btn_avancer, 1, 3)
        layout.addWidget(self.btn_reculer, 1, 1)
        layout.addWidget(self.btn_derouler_stop, 1, 2)
        layout.addWidget(self.btn_aller_debut, 1, 0)
        layout.addWidget(self.btn_aller_fin, 1, 4)
        self.btn_avancer.clicked.connect(self.avancer)
        self.btn_reculer.clicked.connect(self.reculer)
        self.btn_derouler_stop.clicked.connect(self.derouler)
        self.btn_aller_debut.clicked.connect(self.aller_debut)
        self.btn_aller_fin.clicked.connect(self.aller_fin)

    def avancer(self):
        pass

    def reculer(self):
        pass

    def derouler(self):
        pass

    def stopper(self):
        pass

    def aller_fin(self):
        pass

    def aller_debut(self):
        pass


class DialogueCreation(QDialog):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setupUI(parent)
        self.show()

    def setupUI(self, parent):
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
        derouleur.nbr_ruban = int(self.saisie_nbr_ruban.currentText())
        parent.changer_page(PageSaisie)
        self.hide()
        self.deleteLater()


class FenetrePrincipale(QMainWindow):

    def __init__(self):
        super().__init__()
        self.cree_actions()
        self.setupUI()

    def setupUI(self):
        self.cadre_central = PageAccueil(self)
        self.setCentralWidget(self.cadre_central)
        self.cree_menus()
        self.setWindowTitle('Simulateur de Machines de Turing')
        self.setGeometry(100, 200, 300, 450)
        self.show()

    def cree_actions(self):
        self.creer_machine_act = QAction('&Créer une machine', self)
        self.creer_machine_act.triggered \
                              .connect(self.dialogue_creer_machine)
        self.ouvrir_fichier_act = QAction('&Charger une machine', self)
        self.ouvrir_fichier_act.triggered \
                               .connect(self.dialogue_charger_fichier)
        self.sauver_fichier_act = QAction("&Sauvegarder la machine", self)
        self.sauver_fichier_act.triggered.connect(self.dialogue_sauver_fichier)
        self.quitter_act = QAction('&Quitter', self)
        self.quitter_act.triggered.connect(app.quit)

    def cree_menus(self):
        barre_de_menu = self.menuBar()
        barre_de_menu.setNativeMenuBar(False)
        menu_fichiers = barre_de_menu.addMenu('Fichiers')
        menu_fichiers.addAction(self.creer_machine_act)
        menu_fichiers.addAction(self.ouvrir_fichier_act)
        menu_fichiers.addAction(self.sauver_fichier_act)
        menu_fichiers.addAction(self.quitter_act)

    def changer_page(self, page):
        self.cadre_central.deleteLater()
        self.cadre_central = page(self)
        self.setCentralWidget(self.cadre_central)
        self.cadre_central.show()

    def dialogue_sauver_fichier(self):
        chemin = QFileDialog.getSaveFileName(self, 'Open file', 'sauvegarde')
        if chemin[0]:
            contenu = "placeholder"  # machine normalement
            gestion_fichiers.ecriture_fichier_machine(42, contenu, chemin[0])

    def dialogue_charger_fichier(self):
        chemin = QFileDialog.getOpenFileName(self, 'Open file', 'chargement',
                                             "fichiers textes (*.txt *.py)")
        if chemin[0]:
            gestion_fichiers.lecture_fichier_machine(chemin[0])

    def dialogue_creer_machine(self):
        DialogueCreation(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    fenetre = FenetrePrincipale()
    sys.exit(app.exec_())
