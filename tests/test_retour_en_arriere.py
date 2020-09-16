import unittest

from deroul import Derouleur
from machine import Machine
from ruban import Ruban
from typing import List
from type_recurrents import (Clef, Etat, Mouvement, Mouvements, Symbole, Symboles, Transition, Valeur, TypeRuban)


class test_methodes_machine(unittest.TestCase):
    def setUp(self):
        self.derouleurTest = Derouleur()
        Derouleur.etat_courant = Etat('qinit')
        # Initialisation de la liste de rubans
        mot_init1: List[Symbole] = [Symbole('H'), Symbole('E'), Symbole('L'), Symbole('L'), Symbole('O')]
        r1: Ruban = Ruban(mot_init1, TypeRuban.INFINI)
        mot_init2: List[Symbole] = [Symbole('G'), Symbole('O'), Symbole('O'), Symbole('D')]
        r2: Ruban = Ruban(mot_init2, TypeRuban.SEMIFINI)

        self.derouleurTest.rubans = [r1, r2]
        Derouleur.rubans = [r1, r2]

        self.machineTest = Machine()
        self.derouleurTest.machine_courante = self.machineTest
        Derouleur.machine_courante = self.machineTest

        # Creation d'une transition de test
        etat_init: Etat = Etat('q0')
        etat_final: Etat = Etat('qFin')
        symboles_lecture: Symboles = (Symbole('A'), Symbole('B'))
        symboles_ecriture: Symboles = (Symbole('1'), Symbole('2'))
        mouvements: Mouvements = (Mouvement.GAUCHE, Mouvement.DROITE)
        clef: Clef = (etat_init, symboles_lecture)
        valeur: Valeur = (etat_final, symboles_ecriture, mouvements)
        self.transitionTest = (clef, valeur, False, False)



    def test_inverser_regle(self):
        etat_init: Etat = Etat('qFin')
        etat_final: Etat = Etat('q0')
        symboles_lecture: Symboles = (Symbole('1'), Symbole('2'))
        symboles_ecriture: Symboles = (Symbole('A'), Symbole('B'))
        mouvements: Mouvements = (Mouvement.DROITE, Mouvement.GAUCHE)
        clef: Clef = (etat_init, symboles_lecture)
        valeur: Valeur = (etat_final, symboles_ecriture, mouvements)
        transitionInverse = (clef, valeur, False, False)

        self.assertEqual(transitionInverse, self.machineTest.inverser_regle(self.transitionTest))

    def test_appliqer_regle_inverse(self):

        transitionInverse = self.machineTest.inverser_regle(self.transitionTest)
        self.derouleurTest.rubans[0].set_position(3)
        self.derouleurTest.etat_courant = self.machineTest.appliquer_regle_inverse(self.derouleurTest.rubans, transitionInverse)
        motTest: List[Symbole] = [Symbole('H'), Symbole('E'), Symbole('L'), Symbole('L'), Symbole('A')]
        rubanTest = Ruban(motTest,TypeRuban.INFINI)

        # Test si le ruban a ete modifie correctement
        self.assertEqual(rubanTest.symboles, self.derouleurTest.rubans[0].symboles)

        # Test si l'etat courant a ete modifie correctement
        self.assertEqual(Etat('q0'), self.derouleurTest.etat_courant)

    def test_etape_precedente(self):
        self.derouleurTest.pile_regles.append(self.transitionTest)

        self.derouleurTest.etape_precedente()

        motTest: List[Symbole] = [Symbole('A'), Symbole('L'), Symbole('L'), Symbole('O')]
        rubanTest = Ruban(motTest, TypeRuban.INFINI)

        # Test si le ruban a ete modifie correctement
        # Le premier symbole du ruban doit etre supprimé
        # Et le deuxieme doit etre modifie a 'A'
        self.assertEqual(rubanTest.symboles, self.derouleurTest.rubans[0].symboles)

        # Test si l'etat courant a ete modifie correctement
        self.assertEqual(Etat('q0'), self.derouleurTest.etat_courant)

        # Test si la derniere regle utilise a bien ete retiree de la pile
        self.assertEqual([], self.derouleurTest.pile_regles)


