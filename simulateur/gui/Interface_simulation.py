import sys
#from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QGridLayout,
#                            QApplication, QFrame, QComboBox, QVBoxLayout, QHBoxLayout,
#                            QLabel, QPushButton, QListWidget, QDialog,
#                            QCheckBox, QLineEdit, QWidget)
from PyQt5.QtWidgets import *
from typing import List
from PyQt5 import QtCore, QtGui
from derouleur import deroul
import os
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath('../simulateur'))
sys.path.insert(0, os.path.abspath('simulateur/'))
# from simulateur.types_recurrents import (Clef, Etat, Transition, Symbole)

class Simulation(QFrame):
    """
    Page permettant de visualiser et d'actionner le déroulement
    de la simulation.
    Permet d'avancer ou de reculer dans les étapes
    de la simulation.
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.timer = QtCore.QTimer()
        self.setupUI(parent)
        mach = deroul.Derouleur.machine_courante
        deroul.Derouleur.etat_courant = mach.etat_init

    def setupUI(self, parent):

        self.setWindowTitle("Simulation")
        self.setGeometry(450, 200, 700, 400)

        # liste de règles
        self.liste_regles = QListWidget()
        self.lab_regle_utilise = QLabel()
        self.regle_utilise()

        lst_regles = deroul.Derouleur.machine_courante.table_transition
        self.remplir_liste(lst_regles)


        #liste alphabet
        self.liste_alphabet = QLabel("Alphabet: " + self.affiche_alphabet())


        # Zone d'affichage des rubans et de la position
        # de la tête de lecture.
        self.affichage_ruban = AffichageRubans()

        # Message de fin d'exécution, affiche si l'état est final
        # self.affichage_fin = QLabel("resultat et erreur")

        #Boutons de manipulation de la vitesse de l'éxécution
        self.btn_play = QPushButton("play/pause")
        self.btn_avance = QPushButton("avance")
        self.btn_recule = QPushButton("recule")
        self.btn_end = QPushButton("fin")
        self.btn_debut = QPushButton("debut")
        self.btn_avance.clicked.connect(self.avance)
        self.btn_recule.clicked.connect(self.recule)
        self.btn_play.clicked.connect(self.play)
        self.btn_debut.clicked.connect(self.debut)
        self.btn_end.clicked.connect(self.fin)

        # placement
        layout = QVBoxLayout()
        rrhbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("derniere règle utilisée:"))
        vbox.addWidget(self.lab_regle_utilise)
        vbox.addWidget(self.liste_regles)
        vbox.addWidget(self.liste_alphabet)
        rrhbox.addWidget(self.affichage_ruban)
        rrhbox.addLayout(vbox)
        layout.addLayout(rrhbox)
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn_play)
        hbox.addWidget(self.btn_avance)
        hbox.addWidget(self.btn_recule)
        hbox.addWidget(self.btn_end)
        hbox.addWidget(self.btn_debut)
        #hbox.addWidget(self.affichage_fin)
        layout.addLayout(hbox)
        self.setLayout(layout)
        self.show()

    def remplir_liste(self, liste_regle) -> None:
        """
        Remplir la QListWidget avec les règles de la machine.
        """
        for clef, val in liste_regle.items():
            if len(clef[1]) == 1:
                regle = clef[0]+", "+clef[1][0]+" -> "+str(val[0])+", "+str(val[1][0])+", "+str(val[2][0])
            else:
                regle = clef[0]+", "+str(clef[1])+" -> "+str(val[0])+", "+str(val[1])+", "+str(val[2])
            self.liste_regles.addItem(regle)

    def regle_utilise(self) -> None:
        """
        Permet d'afficher la mise à jour de la derniere regle utilisée
        dans l'interface de simulation.
        """
        if deroul.Derouleur.pile_regles:
            self.lab_regle_utilise.setText(str(deroul.Derouleur.pile_regles[-1]))
        else:
            self.lab_regle_utilise.setText("Aucune règle utilisée")

    def avance(self) -> None:
        """ Avance l'exécution de la machine d'une étape. """
        deroul.Derouleur.etape_suivante()
        self.regle_utilise()
        self.affichage_ruban.maj_aff_ruban()

    def recule(self) -> None:
        """ Reviens en arrière d'une étape sur l'exécution. """
        deroul.Derouleur.etape_precedente()
        self.regle_utilise()
        self.affichage_ruban.maj_aff_ruban()

    def debut(self) -> None:
        """ Reviens au début de la simulation. """
        deroul.Derouleur.aller_etape_initial()
        self.regle_utilise()
        self.affichage_ruban.maj_aff_ruban()

    def fin(self) -> None:
        """
        exécute la simulation à la vitesse de l'ordinateur pour
        arriver directement à la fin de l'exécution.
        """
        deroul.Derouleur.aller_etape_final()
        self.regle_utilise()
        self.affichage_ruban.maj_aff_ruban()

    def play(self) -> None:
        """
        deroule étape par étape our stop
        """
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(2000)
            self.timer.timeout.connect(self.avance)

    def afficheResultat(self) -> None:
        """
        Affiche le résultat de l'exécution après
        qu'elle se soit terminé.
        """

    def affiche_alphabet(self):
        """ Affiche l'aphabet de la machine. """
        alph = deroul.Derouleur.machine_courante.extraire_alphabet()
        return ", ".join(map(str, alph))
        
    def stop(self):
        print("fin de l'exécution\n")


class AffichageRubans(QWidget):
    """
    Zone d'affichage des rubans.
    A chaque étape d'exécution met à jour son affichage
    en fonction de qui est reçu par la méthode view des rubans.
    """

    def __init__(self):
        super().__init__()
        self.setupUI()

    def setupUI(self):
        self.setFixedWidth(300)
        self.rubans = deroul.Derouleur.rubans
        nb_rubans = len(self.rubans)
        self.aff_rubans = []
        layout = QVBoxLayout()
        for i in range(nb_rubans):
            ligne = QLabel()
            ligne.setContentsMargins(0, 0, 10, 0)
            self.aff_rubans.append(ligne)
            layout.addWidget(ligne)
        self.setLayout(layout)
        self.maj_aff_ruban()

    @staticmethod
    def format_vu(symboles):
        return "| " + "| ".join(symboles) + " |"

    def maj_aff_ruban(self):
        nbr_symboles = 10
        for i in range(len(self.rubans)):
            symb = AffichageRubans.format_vu(self.rubans[i].view(nbr_symboles))
            self.aff_rubans[i].setText(symb)
