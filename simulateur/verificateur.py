from types_recurrents import Alphabet, Etat, Table_transition, Transition,Symbole,Mouvement
from typing import List
# test
import re

#cette methode verif si le nombre du rubans est entre 1 et 10 ou non
def verif_nb_rubans(nb_ruban):
    """
    Détermine si le nombre de rubans saisi est un nombre strictement
    positif.
    Le type du paramètre peut varier selon l'interface graphique.
    Appelé lorsque l'utilisateur entre le nombre de ruban,
    Utiliser alors pour fixer la variable globale etat_courant
    du module dérouleur
    Exceptions:
        IllegalValue
    """
    a=int(nb_ruban)

    if a in range(1,11):
        return a
    else:
        raise ValueError('le nombre de rubans doit etre entre 1 et 10')

#print(verif_nb_rubans('2'))
#print(type(verif_nb_rubans('6')))


def presence_etat_init(liste_regle: List[str]) -> bool:
    for i in range(0,len(liste_regle)):
        arr = liste_regle[i]
        if arr[::-1]=='I':
            return True

    pass

#cette methode assure que si on lit '$' (fin ruban) dans la partie cl� d'une regle il faut absolument
#rien ecrire et il faut se deplacer � droit
def verif_fin_ruban(regle_saisie,nb_ruban):
    """
    Fonction appelé par verif_format_regle dans le cas des rubans
    semi-finis, et qui détermine si une transition ne réécrit pas
    pas le symbole $, et ne le dépasse pas
    Exceptions:
        IllegalValue
    """
    regle_saisie=regle_saisie.replace(" ", "")
    a=int(nb_ruban)
    b=regle_saisie.find(',')
    Symboles_lus=regle_saisie[b+1:a*2+b]


    for i in range(0,len(Symboles_lus)):

        if(Symboles_lus[i]=='$'):

            num_sy=int((i/2)+1)
            b2=regle_saisie.find('->')
            valeur=regle_saisie[b2+2:]
            valeur2=valeur[valeur.find(',')+1:]
            mouv=valeur2[(a*2):]

            if(valeur2[i]!='*'):
                return False
            else:
                if(mouv[(num_sy-1)*3]!='R'and mouv[(num_sy-1)*3]!='r') :
                    return False
    return True


#print(verif_fin_ruban("e11,$,1,$,0,1->e12,*,*,*,1,0,RI,RI,RI,st,lr",'5'))





#regex états /symbole selon cahier de spécification
etats = "[a-zA-Z0-9_!@*&#]"
#symbole ="[a-zA-Z0-9]"
symbole="^[ /]"
mouvement=""

def verif_format_regle (regle_saisie: str , nbr_ruban:int) -> Transition :
    intial=False
    final=False
    regle=list(regle_saisie)
    for __i__ in range(len(regle)-1):
        # Removing ' '
        if ' ' in regle[__i__]:
            regle[__i__] = regle[__i__].replace(' ', '')
    regle_saisie="".join(regle)

    if(bool(regle_saisie[len(regle_saisie)-1] == 'I') and bool(regle_saisie[len(regle_saisie)-2]=='F') or bool((regle_saisie[len(regle_saisie)-1] == 'F' and regle_saisie[len(regle_saisie)-2]=='I'))):
        regle=list(regle_saisie[0:-3])
        intial=True
        final=True

    elif (regle_saisie[len(regle_saisie)-1] == 'I'):
        regle=list(regle_saisie[0:-2])
        intial=True
    elif (regle_saisie[len(regle_saisie)-1] == 'F'):
        regle=list(regle_saisie[0:-2])
        final=True
    elif (regle_saisie[len(regle_saisie)-1] == ','):
        regle=list(regle_saisie[0:-1])
    else:
        regle=list(regle_saisie)
    
    # Removing unnecessary symbols for compiling
    regle_saisie=''.join(regle)
    # Check for symbol '->'
    assert '->' in regle_saisie, f'(!) Compilation Error. Missing \'->\''

    #split left right side
    x = regle_saisie.split("->")
    left_side=x[0].split(",")
    right_side=x[1].split(",")

    #check caract�re ','
    carac=''
    for i in range (len(left_side)-1):
        if ((left_side[i]==carac )) :
            if ((left_side[i+1]==carac)):
                left_side.pop(i)
                left_side[i] = ','

    #idem
    for i in range (len(right_side)-1):
        if ((right_side[i]==carac )) :
            if ((left_side[i+1]==carac)):

                right_side.pop(i)
                right_side[i] = ','

    ettat_left=[]
    symb_left=[]
    ettat_right=[]
    symb_right=[]
    mouv=[]
    if(bool(re.match(etats, left_side[0])) & bool(re.match(etats, right_side[0])) & verif_fin_ruban(regle_saisie,nbr_ruban)):
        if(len(left_side)-1==nbr_ruban and len(right_side)-len(left_side)==nbr_ruban):
            ettat_left.append(left_side[0])
            ettat_right.append(right_side[0])
            #regex test symbole
            for i in range (1 , len(left_side)):
                if ((not bool(re.match(symbole, left_side[i]))) & len(left_side[i])==1):
                    symb_left.append(left_side[i])
                    continue
                else :
                    assert left_side[i] in symbole ,f'(!) Compilation Error. unkownsymbole '

            for i in range (1 , len(right_side)-nbr_ruban):
                if ((not bool(re.match(symbole, right_side[i]))) & len(right_side[i])==1):
                    symb_right.append(right_side[i])
                    continue
                else :
                    assert right_side[i] in symbole ,f'(!) Compilation Error. unkownsymbole '
            #test mvt
            mvt=right_side[::-1]
            for i in range (0,nbr_ruban):
                if(mvt[i]=='Le' or mvt[i]=='St' or mvt[i]=='Ri'):
                    mouv.append(mvt[i])
                else:
                    assert mvt[i] in mouvement ,f'(!) Compilation Error. mouvement inconnue '
            return ((ettat_left[0], tuple(symb_left)), (ettat_right[0], tuple(symb_right), tuple(mouv[::-1])), intial, final)
        else:
            print( f'(!) Compilation Error. nombre de ruban ne convient pas avec les symbole')
    else:
        assert left_side[0] or right_side[0]  ,f'(!) Compilation Error. etats ou fin de ruban atteint'


#print(verif_format_regle("e,2,1,1   ->q,1,1,1,Le,St,Ri",3 ) )
#print(verif_format_regle("q0,a->q0,b,Ri,   I    F",1))
#verif_fin_ruban("e,2,1,1   ->q,1,1,1,Le,St,Ri",3 )

def verif_etat(etat_a_verifie: Etat) -> Etat:
    if(bool(re.match(etats,etat_a_verifie))):
        return etat_a_verifie
    else:
         assert etat_a_verifie in Etat ,f'(!) Compilation Error. létat passé en paramètre correspond à nos contrainte de nom des états. '



def verif_symboles_saisis(init_ruban: str, alphabet: Alphabet) -> str:
    if(bool(re.match(alphabet,init_ruban))):
         return init_ruban
    else:
         assert init_ruban in alphabet ,f'(!) Compilation Error. symbole ne correspond pas . '




#cette methode determine si le table est non ambigu et deterministe (exempla de ligne refus� : {"e11,1,1":"e11,1,1,st,st"})
def est_deterministe(table_transi):
    """
    Détermine si une table de transition est déterministe, càd
    si elle ne contient pas différentes règles qui à un même
    antécédent associe des images différentes.
    Est appelé dans le module dérouleur.
    """

    liste_keys=list(table_transi.keys())
    LEN=len(liste_keys)
    #partie1
    for i in range(0,LEN):


        for j in range(i+1,LEN):
            if (liste_keys[i]==liste_keys[j]):
                return False

    #partie2
    for cle,valeur in table_transi.items():
        if valeur.find(cle)==0 and valeur.find('R')==-1 and valeur.find('r')==-1 and valeur.find('l')==-1 and valeur.find('L')==-1  :
            return False

    return True


#dect={"a":"ab","a":"ab","ac":"b",'j':'k','ja':'kg'} test partie, toujours vrai car l dectionnaire ecrase un ancien cle si un autre cle de meme valeur est entre
#dect={"e11,1,1":"e11,1,1,st,st"} test partie 2
#print(est_deterministe(dect))


def hello():
    print("Hello from verificateur")


def exemple(a, b):
    return a + b
