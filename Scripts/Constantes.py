#Script comportant toute les constantes majeurs et utilasables du projet (style la grille, la profondeur...)
#Variable de la grille 
GRILLE = [[0, 0, 0, 0, 0, 0, 0] for i in range(6)]
TAILLE_GRILLE = (840, 720)

#Variable generale pour le UI
TAILLE_CASE = 100
ESPACE_CASE = 20
TAILLE_FENETRE = (1300, 800)
POS_GRILLE_X, POS_GRILLE_Y = ((TAILLE_FENETRE[0] - 6 * ESPACE_CASE - 7 * TAILLE_CASE) / 6, (TAILLE_FENETRE[1] - 5 * ESPACE_CASE - 6 * TAILLE_CASE)/2)
POS_COLONES_GRILLE = (80, 200, 320, 440, 560, 680, 800)
DICT_FORCE_REBON = {0 : -2, 1 : -2.5, 2 : -3, 3 : -3.5, 4 : -4.5, 5 : -6}
