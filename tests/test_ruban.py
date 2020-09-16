import unittest
import pytest
from deroul import Derouleur
from machine import Machine
from ruban import Ruban
from typing import List
from type_recurrents import (Clef, Etat, Mouvement, Mouvements, Symbole, Symboles, Transition, Valeur, TypeRuban)

class test_methodes_ruban(unittest.TestCase):
    def setUp(self):
        motInit1: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'), Symbole('T'),
                                  Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        motInit2 = motInit1.copy()
        self.r1 = Ruban(motInit1, TypeRuban.INFINI)
        self.r1.position = 3

        self.r2 = Ruban(motInit2, TypeRuban.SEMIFINI)
        self.r2.position = 3

    def testViewRubanINFINI(self):
        #  Position de la tete:
        #  T  E  S  T  W  O  R  D
        #           ^


        # La methode doit generer une vue partielle du mot.
        expectedView1: List[Symbole] = [Symbole('S'), Symbole('T'),Symbole('W')]
        self.assertEqual(expectedView1,self.r1.view(1))

        expectedView2: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R')]
        self.assertEqual(expectedView2,self.r1.view(3))

        # La methode doit generer une vue en inserant des symboles '_' (Blanc) au debut
        expectedView3: List[Symbole] = [Symbole('_'),Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        self.assertEqual(expectedView3,self.r1.view(4))

        # La methode doit generer une vue en inserant des symboles '_' (Blanc) au debut et a la fin
        expectedView4: List[Symbole] = [Symbole('_'),Symbole('_'),Symbole('_'),
                                        Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R'),
                                        Symbole('D'),Symbole('_'),Symbole('_'),]

        self.assertEqual(expectedView4,self.r1.view(6))

    def testViewRubanSEMIFINI(self):
        #  Position de la tete:
        #  T  E  S  T  W  O  R  D
        #           ^

        # La methode doit generer une vue partielle du mot.
        expectedView1: List[Symbole] = [Symbole('S'), Symbole('T'), Symbole('W')]
        self.assertEqual(expectedView1, self.r2.view(1))

        expectedView2: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R')]
        self.assertEqual(expectedView2, self.r2.view(3))

        # La methode doit generer une vue sans inserer de symboles '_' (Blanc) au debut car le ruban est fini a gauche
        expectedView3: List[Symbole] = [ Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        self.assertEqual(expectedView3, self.r2.view(4))

        # La methode doit generer une vue en inserant des symboles '_' (Blanc) a la fin mais pas au debut
        expectedView4: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'),
                                        Symbole('T'),
                                        Symbole('W'), Symbole('O'), Symbole('R'),
                                        Symbole('D'), Symbole('_'), Symbole('_'), ]

        self.assertEqual(expectedView4, self.r2.view(6))

    def testRecupere_Symbole_Lu(self):
        s: Symbole = Symbole('T')
        self.assertEqual(s,self.r1.recupere_symbole_lu())

    def testEcriture_Symbole(self):
        # Le mot doit etre modifie
        s1: Symbole = Symbole('Z')
        mot1: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'), Symbole('Z'),
                                  Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        self.r1.ecriture_symbole(s1)
        self.assertEqual(mot1,self.r1.symboles)

        # Le mot ne doit pas etre modifie
        s2: Symbole = Symbole('*')
        mot2: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'), Symbole('T'),
                               Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        self.r2.ecriture_symbole(s2)
        self.assertEqual(mot2,self.r2.symboles)

    def testModfier_Position(self):

        self.r1.modifier_position(Mouvement.DROITE)
        self.assertEqual(4,self.r1.position)
        self.r1.modifier_position(Mouvement.GAUCHE)
        self.assertEqual(3, self.r1.position)

        mot1: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'), Symbole('T'),
                               Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D'),
                               Symbole('_')]
        self.r1.set_position(7)
        self.r1.modifier_position(Mouvement.DROITE)
        self.assertEqual(8,self.r1.position)
        self.assertEqual(mot1,self.r1.symboles)

        mot2: List[Symbole] = [Symbole('_'),
                               Symbole('T'), Symbole('E'), Symbole('S'), Symbole('T'),
                               Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D'),
                               Symbole('_')]
        self.r1.set_position(0)
        self.r1.modifier_position(Mouvement.GAUCHE)
        self.assertEqual(0,self.r1.position)
        self.assertEqual(mot2,self.r1.symboles)

        mot3: List[Symbole] = [Symbole('T'), Symbole('E'), Symbole('S'), Symbole('T'),
                               Symbole('W'), Symbole('O'), Symbole('R'), Symbole('D')]
        self.r2.set_position(0)

        with pytest.raises(Exception):
            assert self.r2.modifier_position(Mouvement.GAUCHE)

