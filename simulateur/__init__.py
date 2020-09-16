from types_recurrents import (Clef, Etat, Transition, Symbole)
from typing import List
from .ruban import Ruban
from .machine import Machine

# Le nombre de rubans que la machine emploie etant non fixe,
# regrouper les rubans dans une liste nous permettra d'iterer
# sur les rubans en appliquant notre instructions.
rubans: List[Ruban] = []

# A chaque étape, nous sauvegardons la règle appliquée pour
# permettre le retour en arrière
pile_regles: List[Transition] = []

# L'état courant modifée à chaque étape
etat_courant: Etat = ""

# La Machine correspondant à la simulation à venir ou en cours
machine_courante: Machine = None


def forme_clef(liste_rubans: List[Ruban], etat_actuel: Etat) -> Clef:
    """
    Forme une clef à partir de l'état actuel et
    des rubans.
    """
    symboles_lus: List[Symbole] = tuple([ruban.recupere_symbole_lu()
                                         for ruban in rubans])
    return (etat_actuel, symboles_lus)


def etape_suivante() -> None:
    """
    A partir de la machine, des symboles lu sur les rubans
    et de l'état courant, modifie les rubans et l'état courant.
    Appelé par l'interface graphique, ou par aller_etape_final
    """





def etape_precedente() -> None:
    """
    A partir de la machine et de la pile de regles, permet
    une modification de l'état courant et des rubans équivalent
    à un retour en arrière.
    Appelé par l'interface graphique.
    """
    pass


def aller_etape_initial() -> None:
    """
    Vide la pile de règle, l'état courant revient à l'état initial
    et les rubans reviennent à leur données initiales
    """
    pass


def aller_etape_final() -> None:
    """
    Enchaine l'exécution des étapes jusqu'à atteindre une
    exception de fin d'exécution.
    Utilise l'exception de FinDexecution pour s'arrêter.
    """
    pass


def reinitialise() -> None:
    """
    Les variables globales du dérouleur son remise à leur valeur
    initiale.
    """
    for ruban in rubans :
		ruban.__reset_ruban__()


def Empile(Regle: Transition) -> None:
    """
    Empile la règle mise en paramètre sur la pile 'pile_regles'
    """

