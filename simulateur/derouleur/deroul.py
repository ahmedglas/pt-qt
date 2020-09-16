from types_recurrents import (Clef, Etat, Transition, Symbole)
from typing import List
from .ruban import Ruban
import sys
from .machine import FinExecutionMachine


class Derouleur():
    # Le nombre de rubans que la machine emploie etant non fixe,
    # regrouper les rubans dans une liste nous permettra d'iterer
    # sur les rubans en appliquant notre instructions.
    rubans: List[Ruban] = []
    nb_rubans = 0
    # A chaque étape, nous sauvegardons la règle appliquée pour
    # permettre le retour en arrière
    pile_regles: List[Transition] = []

    # L'état courant modifée à chaque étape
    etat_courant: Etat = ""

    # La Machine correspondant à la simulation à venir ou en cours
    machine_courante = None
    
    #variable qui montre si la machine est fini ou pas
    fin = 0


    @staticmethod
    def forme_clef(liste_rubans: List[Ruban], etat_actuel: Etat) -> Clef:
        """
        Forme une clef à partir de l'état actuel et
        des rubans.
        """
        symboles_lus: List[Symbole] = tuple([ruban.recupere_symbole_lu()
                                             for ruban in Derouleur.rubans])
        return (etat_actuel, symboles_lus)

    @staticmethod
    def etape_suivante() -> None:
        """
        A partir de la machine, des symboles lu sur les rubans
        et de l'état courant, modifie les rubans et l'état courant.
        Appelé par l'interface graphique, ou par aller_etape_final
        """

        try:
            print(Derouleur.rubans)
            print(Derouleur.etat_courant)
            cle_initial = Derouleur.forme_clef(Derouleur.rubans, Derouleur.etat_courant)
            print(cle_initial)
            valeur_a_appliquer = Derouleur.machine_courante.__selection_valeur__(cle_initial)
            Derouleur.etat_courant=Derouleur.machine_courante.appliquer_valeur(valeur_a_appliquer, Derouleur.rubans)
            # la methode appl iquer_valeur fait l'appel aussi au AppliquerChangement
            Derouleur.etat_courant = valeur_a_appliquer[0]  # changement d'etat a voir avec taher si il a deja changer l'etat
            # Empile(Tuple[cle_initial, valeur_a_appliquer, 0, Derouleur.machine_courante.est_sur_etat_final(Derouleur.etat_courant)])
            transition: Transition = [cle_initial, valeur_a_appliquer, False, Derouleur.machine_courante.est_sur_etat_final(Derouleur.etat_courant)]
            Derouleur.Empile(transition)
        except FinExecutionMachine:
                # a voir ca depend avec la partie gui
                states_finaux = Derouleur.machine_courante.etat_finaux
                if(Derouleur.etat_courant in states_finaux):
                    print("\nCette machine s'est termine dans un etat final! Bravo!\n")
                else:
                    print("\nCette machine s'est termine dans un etat non final! Dommage!\n")
                    Derouleur.fin=1
                 




        else:
            # cette depend de l'interface
            """
            symboles_ecrits  = []



            clef = Derouleur.forme_clef(Derouleur.rubans,Derouleur.etat_courant)

            valeur = Derouleur.machine_courante.__selection_valeur(clef)

            transition : Transition = [clef,valeur,False,False]
            Derouleur.Empile(transition)
            Derouleur.etat_courant = Derouleur.machine_courante.appliquer_valeur(valeur)
            """

    @staticmethod
    def etape_precedente() -> None:
        """
        A partir de la machine et de la pile de regles, permet
        une modification de l'état courant et des rubans équivalent
        à un retour en arrière.
        Appelé par l'interface graphique.
        """
        # On retire la derniere regle utilisée du haut de la pile de regles.
        if(Derouleur.pile_regles):
            regle_a_inverser = Derouleur.pile_regles.pop()
            regle_inverse = Derouleur.machine_courante.inverser_regle(regle_a_inverser)
            Derouleur.etat_courant = Derouleur.machine_courante.appliquer_regle_inverse(Derouleur.rubans,
                                                                          regle_inverse)

    @staticmethod
    def aller_etape_initial() -> None:
        """
        Vide la pile de règle, l'état courant revient à l'état initial
        et les rubans reviennent à leur données initiales
        """
        # On vide la pile des regles utilisées.
        Derouleur.pile_regles.clear()

        Derouleur.etat_courant = Derouleur.machine_courante.etat_init
        # Pour chaque ruban, on le remet a son etat initial.
        for ruban in Derouleur.rubans:
            ruban.__reset_ruban__()

    @staticmethod
    def aller_etape_final() -> None:
        """
        Enchaine l'exécution des étapes jusqu'à atteindre une
        exception de fin d'exécution.
        Utilise l'exception de FinDexecution pour s'arrêter.
        """
        while (not (Derouleur.machine_courante.est_sur_etat_final(Derouleur.etat_courant)) and Derouleur.fin==0):
            Derouleur.etape_suivante()
            
        states_finaux = Derouleur.machine_courante.etat_finaux
        if(Derouleur.etat_courant in states_finaux):
            print("\nCette machine s'est termine dans un etat final! Bravo!\n")
        else:
            print("\nCette machine s'est termine dans un etat non final! Dommage!\n")

    @staticmethod
    def reinitialise() -> None:
        """
        Les variables globales du dérouleur son remise à leur valeur
        initiale.
        """
        Derouleur.rubans = []
        Derouleur.nb_rubans = 0

        Derouleur.pile_regles = []
        Derouleur.etat_courant = None

        Derouleur.machine_courante = None

    @staticmethod
    def Empile(Regle: Transition) -> None:
        """
        Empile la règle mise en paramètre sur la pile 'pile_regles'
        """
        #Derouleur.pile_regles.append(Regle)
        try:
            Derouleur.pile_regles.append(Regle)
        except Exception as e:
            print(e)
            print('erreur empile')
