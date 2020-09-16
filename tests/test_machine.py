import unittest
from context import derouleur
from derouleur import Machine
from types_recurrents import Mouvement


class TestExempleSomme(unittest.TestCase):
    def test_undeux(self):
        somme = Machine.exemple(1, 2)
        self.assertEqual(somme, 3)


class TestAjoutTransition(unittest.TestCase):
    def setUp(self):
        self.machine_test = Machine()

    def test_un_ajout_un_ruban(self):
        etat_c, symb_c = "q0", ("0",)
        etat_v, symb_v, mouv = "q1", ("1",), (Mouvement.GAUCHE,)
        init, final = False, False
        transi = ((etat_c, symb_c), (etat_v, symb_v, mouv), init, final)
        self.machine_test.__ajouter_transition__(transi)
        self.assertDictEqual(self.machine_test.table_transition,
                             {(etat_c, symb_c): (etat_v, symb_v, mouv)})
        self.assertFalse(self.machine_test.__table_wildcard__)
        self.assertFalse(self.machine_test.etat_init)
        self.assertFalse(self.machine_test.etat_finaux)

    def test_un_ajout_un_ruban_init(self):
        etat_c, symb_c = "q0", ("0",)
        etat_v, symb_v, mouv = "q1", ("1",), (Mouvement.GAUCHE,)
        init, final = True, False
        transi = ((etat_c, symb_c), (etat_v, symb_v, mouv), init, final)
        self.machine_test.__ajouter_transition__(transi)
        self.assertDictEqual(self.machine_test.table_transition,
                             {(etat_c, symb_c): (etat_v, symb_v, mouv)})
        self.assertFalse(self.machine_test.__table_wildcard__)
        self.assertEqual(self.machine_test.etat_init, etat_c)
        self.assertFalse(self.machine_test.etat_finaux)

    def test_un_ajout_un_ruban_final(self):
        etat_c, symb_c = "q0", ("0",)
        etat_v, symb_v, mouv = "q1", ("1",), (Mouvement.GAUCHE,)
        init, final = False, True
        transi = ((etat_c, symb_c), (etat_v, symb_v, mouv), init, final)
        self.machine_test.__ajouter_transition__(transi)
        self.assertDictEqual(self.machine_test.table_transition,
                             {(etat_c, symb_c): (etat_v, symb_v, mouv)})
        self.assertFalse(self.machine_test.__table_wildcard__)
        self.assertFalse(self.machine_test.etat_init)
        self.assertSetEqual(self.machine_test.etat_finaux, {"q1"})

    def test_deux_ajout_deux_ruban_initialfinal(self):
        etat_c1, symb_c1 = "q0", ("0", "0")
        etat_v1, symb_v1 = "q1", ("1", "1")
        mouv1 = (Mouvement.GAUCHE, Mouvement.DROITE)
        init1, final1 = True, True
        transi1 = ((etat_c1, symb_c1), (etat_v1, symb_v1, mouv1), init1, final1)
        self.machine_test.__ajouter_transition__(transi1)
        etat_c2, symb_c2 = "q3", ("3", "6")
        etat_v2, symb_v2 = "q2", ("2", "4")
        mouv2 = (Mouvement.GAUCHE, Mouvement.DROITE)
        init2, final2 = False, False
        transi2 = ((etat_c2, symb_c2), (etat_v2, symb_v2, mouv2), init2, final2)
        self.machine_test.__ajouter_transition__(transi1)
        self.machine_test.__ajouter_transition__(transi2)
        self.assertDictEqual(self.machine_test.table_transition,
                             {(etat_c1, symb_c1): (etat_v1, symb_v1, mouv1),
                              (etat_c2, symb_c2): (etat_v2, symb_v2, mouv2)})
        self.assertFalse(self.machine_test.__table_wildcard__)
        self.assertEqual(self.machine_test.etat_init, etat_c1)
        self.assertSetEqual(self.machine_test.etat_finaux, {"q1"})

    def test_deux_ajout_deux_ruban_wildcard(self):
        etat_c1, symb_c1 = "q0", ("*", "0")
        etat_v1, symb_v1 = "q1", ("1", "1")
        mouv1 = (Mouvement.GAUCHE, Mouvement.DROITE)
        init1, final1 = False, False
        transi1 = ((etat_c1, symb_c1), (etat_v1, symb_v1, mouv1), init1, final1)
        self.machine_test.__ajouter_transition__(transi1)
        etat_c2, symb_c2 = "q3", ("3", "6")
        etat_v2, symb_v2 = "q2", ("2", "4")
        mouv2 = (Mouvement.GAUCHE, Mouvement.DROITE)
        init2, final2 = False, False
        transi2 = ((etat_c2, symb_c2), (etat_v2, symb_v2, mouv2), init2, final2)
        self.machine_test.__ajouter_transition__(transi1)
        self.machine_test.__ajouter_transition__(transi2)
        self.assertDictEqual(self.machine_test.table_transition,
                             {(etat_c1, symb_c1): (etat_v1, symb_v1, mouv1),
                              (etat_c2, symb_c2): (etat_v2, symb_v2, mouv2)})
        self.assertDictEqual(self.machine_test.__table_wildcard__,
                             {(etat_c1, symb_c1): (etat_v1, symb_v1, mouv1)})
        self.assertFalse(self.machine_test.etat_init, etat_c1)
        self.assertFalse(self.machine_test.etat_finaux)


class TestSelectionValeur(unittest.TestCase):
    def setUp(self):
        self.machine_test = Machine()
        self.clef0 = ("q0", ("0", "0"))
        self.val0 = ("q1", ("1", "1"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.clef1 = ("q1", ("1", "1"))
        self.val1 = ("q2", ("2", "2"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.clef2 = ("q2", ("2", "2"))
        self.val2 = ("q3", ("3", "3"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.machine_test.table_transition = {self.clef0: self.val0,
                                              self.clef1: self.val1,
                                              self.clef2: self.val2}

    def test_clef_existe(self):
        selection = self.machine_test.__selection_valeur__(self.clef1)
        self.assertEqual(selection, self.val1)

    def test_clef_nexistepas(self):
        clef_inconnu = ("q4", ("2", "2"))
        selection = self.machine_test.__selection_valeur__(clef_inconnu)
        # a remplacer par une exception
        self.assertFalse(selection)

    def test_clef_existe_wildcard(self):
        etat_c, symb_c = "q5", ("*", "0")
        etat_v, symb_v = "q6", ("1", "1")
        mouv = (Mouvement.GAUCHE, Mouvement.DROITE)
        init, final = False, False
        val = (etat_v, symb_v, mouv)
        transi = (etat_c, symb_c, etat_v, symb_v, mouv, init, final)
        clef_wild = ("q5", ("8", "0"))
        self.machine_test.__ajouter_transition__(transi)
        selection = self.machine_test.__selection_valeur__(clef_wild)
        self.assertEqual(selection, val)


class TestExtraireAlphabet(unittest.TestCase):
    def setUp(self):
        self.machine_test = Machine()
        self.clef0 = ("q0", ("0", "0"))
        self.val0 = ("q1", ("1", "0"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.clef1 = ("q1", ("1", "1"))
        self.val1 = ("q2", ("2", "3"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.clef2 = ("q2", ("4", "2"))
        self.val2 = ("q3", ("5", "6"), (Mouvement.GAUCHE, Mouvement.DROITE))
        self.machine_test.table_transition = {self.clef0: self.val0,
                                              self.clef1: self.val1,
                                              self.clef2: self.val2}

    def test_alphabet_simple(self):
        alphabet = self.machine_test.extraire_alphabet()
        self.assertSetEqual(alphabet, set(map(str, range(7))))

    def test_alphabet_wildcard(self):
        self.machine_test.table_transition[("q", ("1", "*"))] = self.val0
        alphabet = self.machine_test.extraire_alphabet()
        self.assertSetEqual(alphabet, set(map(str, range(7))))


class TestEstSurEtatFinal(unittest.TestCase):
    def setUp(self):
        self.machine_test = Machine()
        self.machine_test.etat_finaux = {"q0", "qF"}

    def test_contient_final(self):
        self.assertTrue(self.machine_test.est_sur_etat_final("qF"))

    def test_contient_pas_final(self):
        self.assertFalse(self.machine_test.est_sur_etat_final("qf"))
