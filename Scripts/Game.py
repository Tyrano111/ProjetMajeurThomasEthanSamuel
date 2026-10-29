# Il s'occupe de toute la partie calcul et interaction joueur dans le jeu en gros il pourrais y avoir que lui au debut

#Ici on va certainement faire une class de grille qui s'ocupe de tout les calul sur la grille
# Et faire une autre class Jeu qui elle s'occupe de gerer les tours de joueurs, la victoire, les points...

plateau=[[" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "],
         [" "," "," "," "," "," "," "]]

def afficher(plateau):
    for i in range(len(plateau)):
        print(plateau[i])
        

def gagnant_l(plateau, position:tuple, couleur):
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

    
def gagnant_c(plateau, position:tuple, couleur):
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


def position_diagonale_bas(position):
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


def position_diagonale_haut(position):
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

def gagnant_d_bas(plateau, position:tuple, couleur):
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


def gagnant_d_haut(plateau, position:tuple, couleur):
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


def winner(plateau, position:tuple, couleur):
    if gagnant_d_haut(plateau, position, couleur) or gagnant_d_bas(plateau, position, couleur) or gagnant_c(plateau, position, couleur) or gagnant_l(plateau, position, couleur):
        return True
    else:
        return False


def trouve_position(plateau, colonne):
    for i in range(5,-1,-1):
        if plateau[i][colonne]==' ':
            return True, i
    return False, i