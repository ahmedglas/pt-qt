from typing import List
import sys
import os, webbrowser
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath('../simulateur'))
sys.path.insert(0, os.path.abspath('simulateur/'))

from derouleur import Derouleur, Machine, Ruban
import verificateur 
from types_recurrents import Transition
from derouleur import deroul as D


def lecture_fichier_machine(chemin: str) -> None:
    """
    Création d'une machine depuis la lecture d'un fichier dont
    l'emplacement est précisé en paramètre.
    On commence par lire le nombre de ruban qui est vérifié
    par la fonction vérificateur.verif_nbr_rubans.
    Une machine est crée, cette fonction lui donne état initial
    et états finaux en passant par vérificateur.verif_etat.
    Puis les règles sont vérifiés une à une par la fonction
    vérificateur.verif_format_regle. Chaque règle amène
    un appel de la fonction dérouleur.ajouter_transition pour
    les ajouter à la machine.
    """
    try:
        with open(chemin,"r") as fichier:
            print("opened")
            #recuperer toute les lignes sauf celles qui commencent par /     
            contents=[line.strip('\n').rstrip() for line in fichier.readlines() if(("/" not in line.rstrip())and(line.strip('\n').rstrip()!=''))]
            #nbr_rubans = recois la premiere ligne qui = au nombre de rubans verifié
            #et retire la premiere ligne de la liste
            #contents contient la liste des regles
            nbr_rubans=verificateur.verif_nb_rubans(contents.pop(0))
            regles=[line.strip('\n').rstrip() for line in contents if('->' in line)]
            #recherche des etats  
            etat_init=""
            etats_fineau=set()
            for line in regles:
                #clef et valeur
                clef,valeurs=line.split("->")
                clef,valeurs=clef.split(","),valeurs.split(",")
                print("clef "+str(clef) +" valeur "+str(valeurs)+" ")
                #verifie si la fin d'une ligne est = à I ou IF 
                if((valeurs[-1]=="I")or(valeurs[-1]=="IF")):
                    etat_init=clef[0]
                if((valeurs[-1]=="F")or(valeurs[-1]=="IF")):
                    etats_fineau.add(valeurs[0])  
                #fin de la recherche des etats    

            #deroueleur.machine_courrante = une Machine()
            Derouleur.nb_rubans=nbr_rubans
            Derouleur.machine_courante= Machine()                       
            Derouleur.machine_courante.etat_init=etat_init
            Derouleur.machine_courante.etat_finaux=etats_fineau
            Derouleur.machine_courante.remplir_dictionnaire(regles)
            #affichage pour tests
            print("finaux :"+str(etats_fineau))
            print("etat_initial : "+etat_init)
            print("contents+ : "+str(contents))
            print("regles : "+str(regles))
            print("machine :"+str(Derouleur.machine_courante))
            print("machine etats initial: "+str(Derouleur.machine_courante.etat_init))
            print("machine etats finaux :"+str(Derouleur.machine_courante.etat_finaux))
            print("nbr rubans : "+str(Derouleur.nb_rubans))

    except IOError as e:
        print("error : "+str(e.strerror))


def ecriture_fichier_machine(nbr_ruban: int, machine: Machine,
                             chemin: str) -> None:
    """
    Il reste à préciser en fonction de l'interface graphique, si le
    chemin est une chaîne de caractère ou un type spécifique aux
    chemins de fichier.
    Respecte le format précisé pour la sauvegarde de machine,
    récupère état initial, états finaux depuis la machine, ainsi
    que toutes les règles de transitions.

    Écriture fichier dans fichier .txt, dont le nom a été choisi
    par l'utilisateur dans l'interface graphique.
    """
    states_fineau = machine.etat_finaux
    state_init=set([machine.etat_init])    
    try:
        with open(chemin,"w") as file:
            file.writelines(str(nbr_ruban)+"\n")
            for regle in machine.table_transition.items():
                transition=[]
                transition.append(regle[0])
                transition.append(regle[1])
                
                if (state_init.intersection(transition[0])):
                    transition.append(True)
                else:
                    transition.append(False)
                if(states_fineau.intersection(transition[1])):
                    transition.append(True)
                else:
                    transition.append(False)

                file.write(traduire_regle(transition)+'\n')

    except IOError as e:
        print(str(e.strerror))


def sauvegarder_historique_execution(rubans: List[Ruban],
                                     pile_regles: List[Transition]) -> None:
    """
    L'état initial des rubans est récupéré et écrit ligne par ligne
    chaque symbole est séparé par un espace.
    En suite, la règle utilisée à chaque étape de l'exécution
    est récupéré depuis liste_regles et écrite ligne par ligne
    (en respectant le format d'écriture des règles).

    Fonction déclenchée lorsqu'on arrive à une fin d'exécution.
    Écriture dans fichier nommé timestamp.txt.
    """
    try:
        with open("timestamp.txt","w") as file:
            #ecriture des etats initials des rubans
            for ruban in rubans:
                file.write(" ".join(ruban.etat_initial)+"\n")
            #ecriture des regles
            for regle in pile_regles:
                file.write(traduire_regle(regle)+'\n')
    #exceptions            
    except IOError as e:
        print(str(e.strerror))        



def charger_aide() -> None:
    """
    Ouvre une page html d'aide dans le navigateur de l'utilisateur
    """
    webbrowser.open('file://'+os.path.realpath("simulateur/gui/aide.html"))


def traduire_regle(regle: Transition) -> str:
    """
    Cette fonction va traduire une règle en chaine de caractère,
    afin de l'inscrire dans le fichier de sauvegarde.

    Cette fonction va être appelé dans la fonction
    écrire_fichier_machine().
    """
    
    print(regle)
    entres=""
    sorties=""
    clef,valeur=regle[0],regle[1]
    for item in clef:
        entres+=str(item)+","
    for items in valeur:
        sorties+=str(items)+"," 
    entres=entres[0:-1]
    #ecriture sous le format des regles
    resultat=entres+"->"+sorties
    
    resultat = resultat.replace("(","")
    resultat = resultat.replace(",)","")
    resultat = resultat.replace("'","")
    resultat = resultat.replace(")","")
    
    if(regle[2]):
        resultat+="I"
    if(regle[3]):
        resultat+="F"
    print(resultat)
    return resultat

 
