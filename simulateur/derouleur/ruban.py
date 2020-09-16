from typing import List, Set
import re

from types_recurrents import (Clef, Etat, Mouvement, Symbole, Symboles, Transition, Valeur,TypeRuban)


class Ruban():
	
	
    def __init__(self, mot_init, t_ruban) -> None:
        """
        Le premier paramètre est une liste de symboles représentant
        les symboles écrit sur le ruban.
        Le deuxième est la position de la tète sur le ruban.
        Le troisième représente le type du ruban, le choix se
        fera entre ruban semi-fini ou ruban infini.
        """
        self.symboles: List[Symbole] = mot_init
        # remplacer bool par SEMIFINI ou INFINI
        self.type_ruban: TypeRuban = t_ruban

        if(self.type_ruban == TypeRuban.SEMIFINI):
            self.symboles.insert(0,Symbole("$"))

        self.position: int = 0
        self.etat_initial: List[Symbole] = mot_init.copy()

    def view(self, intervalle: int) -> List[Symbole]:
        """
        A destination de l'interface graphique, seule une partie
        du ruban est affichée.
        Cette méthode retourne une sous liste de la liste
        représentant les symboles sur le ruban.
        Cette sous liste comprend les symboles dans
        l'intervalle centré sur position et de longueur 2x taille vue.
        La méthode devra s'adapter et inclure des symboles blancs
        si la vue est plus grande que le ruban, pour remplir
        les vides dans la sous liste.
        """
        vue: List[Symbole] = []
        i = intervalle - self.position

        # Symboles dans [  position - intervalle  ,  position  [
        if(self.type_ruban == TypeRuban.INFINI):
            # Vue pour un Ruban Infini
            while (0 < i):
                # Creation de symbole blanc pour remplir la vue
                vue.append(Symbole("_"))
                i -= 1
            # Insertion des symboles d'index allant de i a position-1
            vue.extend(self.symboles[-i: self.position])
        else:
            # Vue pour un Ruban Semifini
            if(0 < i ):
                vue.extend(self.symboles[0:self.position])
            else:
                vue = self.symboles[-i:self.position]



        vue.append(self.recupere_symbole_lu())

        i = self.position + intervalle

        # Symboles dans ]  position  ,  position + intervalle ]

        if (i < len(self.symboles)):
            vue.extend(self.symboles[self.position + 1:self.position + intervalle + 1])
        else:
            vue.extend(self.symboles[self.position + 1: len(self.symboles)])
            j = self.position + intervalle + 1 - len(self.symboles)
            while (0 < j):
                vue.append(Symbole("_"))
                j -= 1

        return vue

    def recupere_symbole_lu(self) -> Symbole:
        """
        Renvoie le symbole correspondant à la position de
        la tête de lecture.
        """
        return self.symboles[self.position]

    def ecriture_symbole(self, s: Symbole) -> None:
        """
        Cette méthode modifie le symbole qui se trouve à la position
        de la tête de lecture et le remplace par le symbole s passé
        en paramètre.
        Si symbole est une wildcard, le symbole n'est pas remplacé.
        """
        if(s != Symbole('*')):
            self.symboles[self.position] = s

    def __reset_ruban__(self) -> None:
        """
        Remet le ruban a l'etat initial de l'execution.
        Et place la tete de lecture a la position 0.
        """
        print(self.etat_initial)
        self.symboles = self.etat_initial.copy()
        self.position = 0

    def modifier_position(self, mouvement: Mouvement) -> None:
        """
        Cette méthode modifie la position de la tête de lecture
        en fonction du mouvement, droite, gauche ou sur place donnée
        """
        if mouvement == Mouvement.DROITE:
            self.position += 1
            if (self.position == len(self.symboles)):
                # La machine a atteint l'extremité du ruban a droite,il faut creer un nouveau symbole blanc sur le ruban.
                self.symboles.append(Symbole("_"))
        elif mouvement == Mouvement.GAUCHE:
            if (self.position == 0):
                if (self.type_ruban == TypeRuban.SEMIFINI):
                    raise Exception(
                        'La machine tente de se deplacer vers la gauche alors qu\'elle a atteint la fin du ruban.')
                else:
                    # La machine a atteint l'extremité gauche du ruban, on insert un symbole blanc a gauche.
                    self.symboles.insert(0, Symbole("_"))
            else:
                self.position -= 1

    def appliquer_changement(self, mouvement: Mouvement, s: Symbole) -> None:
        """
        Reçoit le mouvement et le symbole correspondant à la
        transition appliquée pour ce ruban.
        Utilise les méthodes privés, modifier_position et
        ecriture_symbole.
        """
        self.ecriture_symbole(s)
        self.modifier_position(mouvement)
