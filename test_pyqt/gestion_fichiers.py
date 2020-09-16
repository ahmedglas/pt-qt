def lecture_fichier_machine(chemin) -> None:
    """
    Création d'une machine depuis la lecture d'un fichier dont
    l'emplacement est précisé en paramètre.
    On commence par lire le nombre de ruban qui est vérifié
    par la fonction verificateur.verif_nbr_rubans.
    Une machine est crée, cette fonction lui donne état initial
    et états finaux en passant par verificateur.verif_etat.
    Puis les règles sont vérifiés une à une par la fonction
    verificateur.verif_format_regle. Chaque règle amène
    une appel de la fonction derouleur.ajouter_transition pour
    les ajouter à la machine.
    """
    print("Chargement fait")
    with open(chemin, 'r') as f:
        print(f.read())


def ecriture_fichier_machine(nbr_ruban, machine, chemin) -> None:
    """
    Il reste à préciser en fonction de l'interface graphique, si le
    chemin est une chaîne de caractère ou un type spécifique aux
    chemins de fichier.
    Respecte le format précisé pour la sauvegarde de machine,
    récupère état initial, états finaux depuis la machine, ainsi
    que toutes les règles de transitions.

    Ecriture fichier dans fichier .txt, dont le nom a été choisi
    par l'utilisateur dans l'interface graphique.
    """
    print("Sauvegarde faite")
    with open(chemin, 'w') as f:
        f.write(machine)


def sauvegarder_historique_execution(rubans, pile_regles) -> None:
    """
    L'état initial des rubans est récupéré et écrit ligne par ligne
    chaque symbole est séparé par un espace.
    En suite, la règle utilisée à chaque étape de l'exécution
    est récupéré depuis liste_regles et écrite ligne par ligne
    (en respectant le format d'écriture des règles).

    Ecriture dans fichier nommé timestamp.txt.
    """
    pass


def charger_aide() -> None:
    """
    Ouvre une page html d'aide dans le navigateur de l'utilisateur
    """
    pass


def traduire_regle(regle) -> str:
    """
    Cette fonction va traduire une règle en chaine de caractère,
    afin de l'inscrire dans le fichier de sauvegarde.

    Cette fonction va être appelé dans la fonction
    écrire_fichier_machine().
    """
    pass
