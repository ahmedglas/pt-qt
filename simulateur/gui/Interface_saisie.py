from PyQt5.QtWidgets import (QMainWindow, QAction, QFileDialog, QGridLayout,
                             QApplication, QFrame, QComboBox, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QListWidget, QDialog,
                             QCheckBox, QLineEdit, QWidget)

import sys
from derouleur import Derouleur, Machine, Ruban
from typing import List
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from Interface_simulation import *

class Saisie(QFrame):
    
    types_rub = 0
    
    def __init__(self,parent):
        super().__init__(parent)
        self.setUI(parent)
    
    def setUI(self, parent):

        self.setStyleSheet('background: rgb(233,150,122)')
        parent.resize(640,480)
		
        #Case à cocher pour 'état initial' et 'état final'
        self.init = QCheckBox("etat init")
        self.final = QCheckBox("etat final")
        
        #zone de texte des règles
        self.label_regle = QLabel("Règles:")
        self.texte_regle = QLineEdit()
        self.texte_regle.setStyleSheet('background: rgb(255,255,255)')
        
        #zone de texte de l'initialisation des rubans
        self.label_init_ruban = QLabel("Initialisation des rubans:")
        self.layout_init_ruban = QVBoxLayout()
        texte_init_ruban = QLineEdit()
        self.liste_init = []
        
        i=0
        while i<Derouleur.nb_rubans:
            self.liste_init.append(QLineEdit())
            i+=1
        
        i=0
        while i<Derouleur.nb_rubans:
            self.liste_init[i].setStyleSheet('background: rgb(255,255,255)')
            self.layout_init_ruban.addWidget(self.liste_init[i])
            i+=1
        
         #zone d'affichage des règles déjà rentrées
        self.liste = QListWidget()
        self.liste.setStyleSheet('background: rgb(255,255,255)') 
        
        #bouton d'ajout à la liste
        self.bouton_valid = QPushButton("Ajouter", self)     
        self.bouton_valid.clicked.connect(lambda: self.ajout_Item(self.texte_regle.text(), self.liste, self.init, self.final))
        self.bouton_valid.setStyleSheet('background: rgb(255,255,255)')
        
        #bouton de suppression d'une règle dans la Qliste
        self.bouton_supp = QPushButton("supp", self) 
        self.bouton_supp.clicked.connect(lambda: self.liste.takeItem(self.liste.currentRow()))
        self.bouton_supp.setStyleSheet('background: rgb(255,255,255)')

        #bouton qui retourne la liste des règles
        self.bouton_go = QPushButton("Lancer", self)
        self.bouton_go.clicked.connect(lambda: self.lancer_machine(self.liste, self.liste_init, parent))
        self.bouton_go.setStyleSheet('background: rgb(255,255,255)')
        
        layout = QVBoxLayout()
        layoutCk = QVBoxLayout()
        layoutRgl = QHBoxLayout()
        layoutfin = QHBoxLayout()
        
        layout.addWidget(self.label_init_ruban)
        layout.addLayout(self.layout_init_ruban)
        
        layoutCk.addWidget(self.init)
        layoutCk.addWidget(self.final)
        layoutCk.setAlignment(self.init, Qt.AlignBottom)
        layoutCk.setAlignment(self.final, Qt.AlignTop)
        
        layoutRgl.addWidget(self.label_regle)
        layoutRgl.addWidget(self.texte_regle)
        layoutRgl.addLayout(layoutCk)
        layoutRgl.addWidget(self.bouton_valid)
        layoutRgl.addWidget(self.liste)
        layout.addLayout(layoutRgl)
        
        layoutfin.addWidget(self.bouton_supp)
        layoutfin.addWidget(self.bouton_go)
        layout.addLayout(layoutfin)
        
        
        self.setLayout(layout)
        if Derouleur.machine_courante:
            self.init_liste(self.liste)

    def cons_liste(self, liste:QListWidget) -> List[str]:
        """
        Construit une liste de règles et la retourne
        """
        liste_res = []
        i = 0
        while liste.item(i):
            res = liste.item(i)
            liste_res.append(res.text())
            i += 1
        print(liste_res)
        return liste_res
        
    def init_liste(self,liste:QListWidget):
        """
        Initialise la liste de règles lorsqu'on charge depuis un fichier.
        """
        states_finaux = Derouleur.machine_courante.etat_finaux
        state_init=set([Derouleur.machine_courante.etat_init]) 
        for regle in Derouleur.machine_courante.table_transition.items():
            regle_str = str(regle)
                
            #formatage des regles
            regle_str = regle_str.replace(")), ", "->")
            regle_str = regle_str.replace(")),", "->")
            regle_str = regle_str.replace(",)", "")
            regle_str = regle_str.replace(")", "")
            regle_str = regle_str.replace("(", "")
            regle_str = regle_str.replace("',", "")
            regle_str = regle_str.replace("'", "")
            regle_str = regle_str.replace(" ", ",")
            
            #Rajout de I ou/et F à la fin de la règle
            transition=[]
            transition.append(regle[0])
            transition.append(regle[1])
            
            if(state_init.intersection(transition[0]) and states_finaux.intersection(transition[1])):
                regle_str+=',IF'
            elif (state_init.intersection(transition[0])):
                regle_str+=',I'
            elif(states_finaux.intersection(transition[1])):
                regle_str+=',F'
            
            liste.addItem(regle_str)

        
    def ajout_Item(self, item:str, liste:QListWidget, init:QCheckBox, final:QCheckBox) -> None:
        """
        Ajoute une règle dans la Qliste qui est affiché et vérifie si la règle n'est pas vide. Ajoute 'I' à 'Item' si 'init' est coché et un 'F' si 'final' est coché.
        """
        tmp = 0
        if init.isChecked():
            if tmp==0: 
                item+=','
                tmp = 1
            item += 'I'
            
			
        if final.isChecked():
            if tmp==0: 
                item+=','
                tmp = 1
            item += 'F'
		
        if len(item) > 0:
            liste.addItem(item)
            
    def lancer_machine(self, liste:QListWidget, liste_init:list, parent):
        """
        Transforme 'liste' en une liste python lisible pour le dérouleur en appelant 'cons_liste'. Transforme le 'texte_init_ruban' en un str lisible pour le dérouleur. Donne ensuite ses données au dérouleur en appelant 'remplir_dictionnaire'
        Passe à la page de simulation.
        """
        i=0
        err=0
        while i<Derouleur.nb_rubans:
            if (liste_init[i].text()!=""):
                Derouleur.rubans.append(Ruban(list(liste_init[i].text()), self.types_rub))
            else:
                print("erreur: il manque une initialisation des rubans")
                err =1
            i+=1
        if(err==0):
            Derouleur.machine_courante=Machine()
            Derouleur.machine_courante.remplir_dictionnaire(self.cons_liste(liste))
            parent.changer_page(Simulation)
               
               

