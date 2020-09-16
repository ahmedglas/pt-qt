from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QGridLayout,
                             QApplication, QFrame, QComboBox, QVBoxLayout,
                             QLabel, QPushButton, QListWidget, QDialog,
                             QCheckBox, QLineEdit, QWidget)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
import sys

class Accueil(QFrame):
    """
    Page d'accueil de l'interface graphique.
    Contient trois boutons, créer une machine, 
    charger une machine, quitter.
    
    Utilise les méthodes de sa fenêtre parent 
    pour permettre d'afficher les dialogues de 
    ces actions.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUI(parent)

    def setupUI(self, parent):
        
        self.setStyleSheet('background: rgb(105,150,156)')
         
        #Bouton pour créer une nouvelle machine
        self.btn_nv_machine = QPushButton("Créer une nouvelle machine", self)
        self.btn_nv_machine.setIcon(QIcon('gui/Icon/image_new.png'))
        self.btn_nv_machine.setIconSize(QSize(50,50))
        self.btn_nv_machine.clicked.connect(parent.dialogue_creer_machine)
                           
        #Bouton pour charger une machine depuis un fichier
        self.btn_charger_machine = QPushButton("Charger une machine", self)
        self.btn_charger_machine.setIcon(QIcon('gui/Icon/image_charger.png'))
        self.btn_charger_machine.setIconSize(QSize(50,50))
        self.btn_charger_machine.clicked \
                                .connect(parent.dialogue_charger_fichier)
        
        #Bouton pour quitter l'application
        self.btn_quitter = QPushButton("Quitter", self)
        self.btn_quitter.clicked.connect(parent.quitter_appli)
        
        layout = QVBoxLayout()
        #layout.addWidget(self.image)
        layout.addWidget(self.btn_nv_machine)
        layout.addWidget(self.btn_charger_machine)
        layout.addWidget(self.btn_quitter)
        self.setLayout(layout)

