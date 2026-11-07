# Il s'occupe de toute la partie calcul et interaction joueur dans le jeu en gros il pourrais y avoir que lui au debut

#Ici on va certainement faire une class de grille qui s'ocupe de tout les calul sur la grille
# Et faire une autre class Jeu qui elle s'occupe de gerer les tours de joueurs, la victoire, les points...

<<<<<<< HEAD
import ConstantesEtVariable as CV
=======
from ctypes import Union
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9


plateau=[[" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "]]

def afficher(plateau : list):
    for i in range(len(plateau)):
        print(plateau[i])
        

def gagnant_l(plateau : list, position : tuple, couleur : str) -> bool:
    """Vérifie si le dernier coup a permis de gagner sur la ligne"""
    ligne=position[0]
    n=0
    for i in range(7):
        if couleur==plateau[ligne][i]:
            n=n+1
        else:
            n=0
        if n==4:
            return True
    return False

    
def gagnant_c(plateau : list, position : tuple, couleur : str) -> bool:
    """Vérifie si le dernier coup a permis de gagner sur la colonne"""
    n=0
    colonne=position[1]
    for i in range(6):
        if couleur==plateau[i][colonne]:
            n=n+1
        else:
            n=0
        if n==4:
            return True
    return False


def position_diagonale_bas(position : tuple) -> list:
    '''Renvoie la position de la case la plus basse de la diagonale montante passant par la position donnée'''
    ligne=position[0]
    colonne=position[1]
    position_bas=[]
    if 5-ligne<=colonne:
        position_bas.append(5)
        position_bas.append(colonne-(5-ligne))
    else:
        position_bas.append(5-colonne)
        position_bas.append(0)
    return position_bas


def position_diagonale_haut(position : tuple) -> list:
    '''Renvoie la position de la case la plus haute de la diagonale descendante passant par la position donnée'''
    ligne=position[0]
    colonne=position[1]
    position_haut=[]
    if ligne<=colonne:
        position_haut.append(0)
        position_haut.append(colonne-ligne)
    else:
        position_haut.append(ligne-colonne)
        position_haut.append(0)
    return position_haut

def gagnant_d_bas(plateau : list, position : tuple, couleur : str) -> bool:
    '''Vérifie si le dernier coup a permis de gagner sur la diagonale montante'''
    position_bas=position_diagonale_bas(position)
    ligne=position_bas[0]
    colonne=position_bas[1]
    n=0
    deplacement_min=min(6-colonne,ligne)
    for i in range(deplacement_min+1):
        if couleur==plateau[ligne-i][colonne+i]:
            n=n+1
        else:
            n=0
        if n==4:
            return True
    return False  


def gagnant_d_haut(plateau : list, position : tuple, couleur : str) -> bool:
    '''Vérifie si le dernier coup a permis de gagner sur la diagonale descendante'''
    position_haut=position_diagonale_haut(position)
    ligne=position_haut[0]
    colonne=position_haut[1]
    n=0
    deplacement_min=min(6-colonne,5-ligne)
    for i in range(deplacement_min+1):
        if couleur==plateau[ligne+i][colonne+i]:
            n=n+1
        else:
            n=0
        if n==4:
            return True
    return False  


def winner(plateau : list, position : tuple, couleur : str) -> bool:
    '''Vérifie si le dernier coup a permis de gagner'''
    if gagnant_d_haut(plateau, position, couleur) or gagnant_d_bas(plateau, position, couleur) or gagnant_c(plateau, position, couleur) or gagnant_l(plateau, position, couleur):
        return True
    else:
        return False


<<<<<<< HEAD
def trouve_position(plateau : list, colonne : int, couleur : str) -> tuple:
    '''Renvoie la position de la case la plus basse de la colonne donnée'''
    if plateau[0][colonne] != "." + couleur:
=======
def trouve_position(plateau : list, colonne : int) -> tuple:
    '''Renvoie la position de la case la plus basse de la colonne donnée'''
    if plateau[0][colonne] != ".":
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9
        for i in range(5,-1,-1):
            if plateau[i][colonne]==' ':
                return True, i
    return False, 0


<<<<<<< HEAD
def bloque_colonne(colonne : int, couleur : str) -> list:
=======
def bloque_colonne(plateau : list, colonne : int, couleur : str) -> list:
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9
    '''Bloque la colonne donnée lors de son tour et celui de l'adversaire'''
    couleur_adverse=""
    if couleur=="r":
        couleur_adverse="j"
    else:
        couleur_adverse="r"
<<<<<<< HEAD
    if CV.grille[0][colonne] == " " or CV.grille[0][colonne] == f".{couleur_adverse}":
        CV.grille[0][colonne] = f".{couleur}"
    return CV.grille

def desbloque_colonne(couleur : str) -> list:
    '''Débloque la colonne bloquée lors de son tour précédant'''
    for i in range(7):
        if CV.grille[0][i]== f".{couleur}":
            CV.grille[0][i]= " " 
    return CV.grille

def fantome(position : tuple, couleur : str):
=======
    if plateau[0][colonne] == " " or plateau[0][colonne] == f".{couleur_adverse}":
        plateau[0][colonne] = f".{couleur}"
    return plateau

def desbloque_colonne(plateau : list, couleur : str) -> list:
    '''Débloque la colonne bloquée lors de son tour précédant'''
    for i in range(7):
        if plateau[0][i]== f".{couleur}":
            plateau[0][i]= " " 
    return plateau

def fantome(plateau : list, position : tuple, couleur : str)-> Union[tuple, str]:
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9
    '''Place un fantôme de la couleur donnée à la position donnée'''
    ligne=position[0]
    colonne=position[1]
    if CV.grille[ligne][colonne]==" "  and CV.grille[0][colonne]!='.r' and CV.grille[0][colonne]!='.j':
        CV.grille[ligne][colonne]='f'+couleur
        return CV.grille, (ligne, colonne)
    else:
        return 'position indisponible'

<<<<<<< HEAD
def desbloque_fantome(position : tuple):
=======
def desbloque_fantome(plateau : list, position : tuple)-> Union[bool, tuple]:
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9
    '''Change le fantôme en jeton classique à la position donnée si il y a un jeton sous le fantôme'''
    ligne=position[0]
    colonne=position[1]
    if ligne==0:
        return None
<<<<<<< HEAD
    if CV.grille[ligne-1][colonne]=="fr":
        CV.grille[ligne-1][colonne]= "r"
        return (ligne-1,colonne), 'r'
    if CV.grille[ligne-1][colonne]== "fj":
        CV.grille[ligne-1][colonne]= "j"
        return (ligne-1,colonne), 'j'
    return None, None
=======
    if plateau[ligne-1][colonne]=="fr":
        plateau[ligne-1][colonne]= "r"
        return plateau, (ligne-1,colonne)
    if plateau[ligne-1][colonne]== "fj":
        plateau[ligne-1][colonne]= "j"
        return plateau, (ligne-1,colonne)
>>>>>>> eda78593c8866e319a0088e5cf39226f1f4cc1c9
