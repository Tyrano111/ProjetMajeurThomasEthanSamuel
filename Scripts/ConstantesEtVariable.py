#Script comportant toute les constantes majeurs et utilasables du projet (style la grille, la profondeur...)
#Variable de la grille 
TAILLE_GRILLE = (840, 720)

#Variable generale pour le UI
TAILLE_CASE = 120
TAILLE_FENETRE = (1300, 800)
POS_GRILLE_X, POS_GRILLE_Y = ((TAILLE_FENETRE[0] -  7 * TAILLE_CASE) / 6, (TAILLE_FENETRE[1] - 6 * TAILLE_CASE)/2)
POS_COLONES_GRILLE = (80, 200, 320, 440, 560, 680, 800)
DICT_FORCE_REBON = {0 : -2, 1 : -2.5, 2 : -3, 3 : -3.5, 4 : -4.5, 5 : -6}

#Variable pour l'IA
AI_DEPTH=6

FENETRES={}
def construire_fenetres(ligne, colonne):
    #Les fenêtres de 4 horizontales, verticales et diagonales
    l_fenetre = []
    for l in range(ligne): #Horizontales
        for c in range(colonne - 3):
            l_fenetre.append(tuple((l, c + k) for k in range(4)))
    for c in range(colonne): #Verticales
        for l in range(ligne - 3):
            l_fenetre.append(tuple((l + k, c) for k in range(4)))
    for l in range(ligne - 3): #Diagonales
        for c in range(colonne - 3):
            l_fenetre.append(tuple((l + k, c + k) for k in range(4)))
            l_fenetre.append(tuple((l + 3 - k, c + k) for k in range(4)))
    FENETRES[(ligne, colonne)] = l_fenetre
    return l_fenetre
FENETRES = construire_fenetres(6, 7)

POIDS = {("j",4): 10000, ("j", 3): 50,  ("j", 2): 10,  ("j", 1): 1,
         ("r",4): 10000, ("r", 3): -75, ("r", 2): -11, ("r", 1): -1}