from typing import List, Set
import re

from types_recurrents import (Alphabet, Clef, Etat, FinExecutionMachine,
                              Mouvement, Symboles, Table_transition,
                              Transition, Valeur)
from derouleur.ruban import Ruban
from verificateur import verif_format_regle, presence_etat_init
from derouleur.deroul import Derouleur


class Machine():

    def __init__(self):
        self.etat_init: Etat = ""
        self.etat_finaux: Set[Etat] = set()
        self.table_transition: Table_transition = dict()
        # contient les wildcars pour permettre une recherche linéaire
        # plus rapide
        self.__table_wildcard__: Table_transition = dict()

    def remplir_dictionnaire(self, liste_regle: List[str]) -> None:
        """
        Remplie le dictionnaire avec la liste de règles provenant de
        l'interface graphique ou d'un fichier en paramètre.
        Utilise la fonction 'ajouter_transition'.
        Remplie en même temps les états finaux et l'état initial.
        """
        presence_etat_init(liste_regle)
        for regle in liste_regle:
            self.__ajouter_transition__(verif_format_regle(regle, Derouleur.nb_rubans))

    def __ajouter_transition__(self, regle_saisie: Transition) -> None:
        """
        Ajoute la 'regle_saisie' dans le dictionnaire.
        Est appelé dans la fonction 'remplir_dictionnaire'
        """
        # On suppose que le type Transition contiendra
        # l'information sur les états finaux et l'état initial
        clef, val, init, final = regle_saisie
        etat_clef, symb_clef = clef
        etat_val, symb_val, mouv = val
        self.table_transition[clef] = val
        # s'il y a une wildcard (*), on l'ajoute au dictionnaire
        # les stockant
        if "*" in str(symb_clef) or "*" in str(symb_val):
            self.__table_wildcard__[clef] = val
        if init:
            self.etat_init = etat_clef
        if final:
            self.etat_finaux.add(etat_val)

    def __selection_valeur__(self, clef: Clef) -> Valeur:
        """
        Cette fonction sélectionne la valeurs a appliquer dans
        la table de transitions.
        Si la clé ne correspond a aucun élément, None est envoyé
        et l'exception doit être gérer. (arrêt de la machine)
        Exception:
            FinExecutionMachine
        """
        if clef in self.table_transition:
            return self.table_transition[clef]
        else:
            # on fait un recherche linéaire dans les clefs avec wildcard
            # cette recherche se fait en utilisant les expressions
            # régulières
            clef_str = str(clef)
            for k in self.__table_wildcard__:
                # on transforme la clef en str et on échappe tout les
                # caractères spéciaux
                k_reg = re.escape(str(k))
                # une * va correspondre à n'importe quoi, c'est donc un .
                # qui ne doit pas être échappé
                k_reg = k_reg.replace("\*", ".")
                if re.search(k_reg, clef_str):
                    return self.__table_wildcard__[k]
        raise FinExecutionMachine("Fin de l'exécution")

    def appliquer_valeur(self, valeur: Valeur,
                         listeRubans: List[Ruban]) -> Etat:
        """
        A partir de la valeur extraite de la fonction
        précédente, on procède au déroulement de la machine,
        c'est a dire : écrire les symboles sur les rubans,
        bouger les têtes de lectures et changer l'état courant
        de la machine
        """


        i: int = 0
        # Parcours de la liste de rubans.
        while i < (len(valeur[1])):
            # On appelle la methode qui permet l'ecriture et le mouvement sur le ruban.
            listeRubans[i].appliquer_changement(Mouvement(valeur[2][i]), valeur[1][i])
            i += 1
        # On retourne le nouvel etat de la machine
        return valeur[0]

    def inverser_regle(self, regle: Transition) -> Transition:
        """
        retourne la transition à appliquer pour revenir à l'étape
        précédente de l'exécution de la machine.
        """

        etat_debut: Etat = regle[1][0]  # = regle[Valeur][Etat]
        symboles_lecture: Symboles = regle[1][1]  # = regle[Valeur][Symboles]

        etat_fin: Etat = regle[0][0]  # = regle[Clef][Etat]
        symboles_ecriture: Symboles = regle[0][1]  # = regle[Clef][Symboles]
        mouvements: List[Mouvement] = []

        for m in regle[1][2]:  # parcours de regle[Valeur][Mouvements]
            if m == 'Ri':
                mouvements.append(Mouvement.GAUCHE)
            elif m == 'Le':
                mouvements.append(Mouvement.DROITE)
            else:
                mouvements.append(Mouvement.SUR_PLACE)

        regle_inverse: Transition = ((etat_debut, symboles_lecture), (etat_fin, symboles_ecriture, tuple(mouvements)),False,False)

        return regle_inverse

    def appliquer_regle_inverse(self, listeRubans: List[Ruban],
                                transition: Transition) -> Etat:
        """
        Appliquer une règle inversée a la machine.
        Le traitement est différent entre les règles normales et
        les règles inversées, car dans le cas des règles inversées,
        le mouvement des têtes doit s'effectuer avant l'écriture.
        """


        j = len(listeRubans) -1
        while (0 <= j):
            ruban = listeRubans[j]
            i = ruban.position
            
            ruban.modifier_position(transition[1][2][j])

            # Ecriture du symbole sur le ruban apres le mouvement.
            ruban.ecriture_symbole(transition[1][1][j])
            j -= 1
        # On retourne le nouvel etat de la machine apres l'application de la regle.
        return transition[1][0]

    def extraire_alphabet(self) -> Alphabet:
        """
        Renvoie l'ensemble des symboles contenus dans
        les règles de transition.
        """
        alphabet: Alphabet = set()
        for clef, val in self.table_transition.items():
            alphabet = alphabet.union(set(clef[1] + val[1]))
        # La wildcard n'est pas un élément de l'alphabet
        alphabet.discard("*")
        return alphabet

    def est_sur_etat_final(self, etat_courant: Etat) -> bool:
        """
        Déterminer si l'état courant est final. Appelé
        lors de la fin de l'exécution.
        """
        return etat_courant in self.etat_finaux
