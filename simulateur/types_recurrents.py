from typing import NewType, Tuple, Set, Dict
from enum import Enum

Etat = NewType("Etat", str)

# Un symbole est une chaîne de longueur 1
Symbole = NewType("Symbole", str)
# Symboles contient nbr_rubans x Symbole
Symboles = Tuple[Symbole, ...]


class Mouvement(Enum):
    """ # Définition des mouvements par une énumération """
    GAUCHE = 'Le'
    SUR_PLACE = 'St'
    DROITE = 'Ri'


class TypeRuban(Enum):
    """ # Définition des types de ruban par une énumération """
    INFINI = 0
    SEMIFINI = 1


# Mouvements contient nbr_rubans x Symbole
Mouvements = Tuple[Mouvement, ...]

# Clef correspond à l'entrée de la fonction de transition
Clef = Tuple[Etat, Symboles]
# Une valeur correspond à la sortie de la fonction de transition
Valeur = Tuple[Etat, Symboles, Mouvements]
# Une transition associe à un état et aux symboles lus
# un nouvel état, des symboles à écrire et les prochains mouvements
# le premier booléen indique si la chaine contient l'état initial
# le second s'il contient un état final
Transition = Tuple[Clef, Valeur, bool, bool]
# Une table de transition est un tableau associatif
# associant à une clef une valeur
Table_transition = Dict[Clef, Valeur]

# Un Alphabet est l'ensemble des symboles que l'on trouve dans
# dans la table de transition.
# Si le ruban est semi-infini, il contient le symbole $
Alphabet = Set[Symbole]


class FinExecutionMachine(Exception):
    """
    Exception soulevé lorsqu'aucune transition n'est trouvée.
    Cela veut dire que la machine est arrivée à la fin
    de son exécution.
    """
    pass
