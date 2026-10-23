#Script comportant toute les constantes majeurs et utilasables du projet (style la grille, la profondeur...)
#Variable de la grille 
GRILLE = [ [0, 0, 0, 0, 0, 0, 0] for i in range(6)]

#Variable generale pour le UI
TAILLE_CASE = 75
ESPACE_CASE = 15
TAILLE_FENETRE = (800, 600)
POS_GRILLE_X, POS_GRILLE_Y = ((TAILLE_FENETRE[0] - 6 * ESPACE_CASE - 7 * TAILLE_CASE) / 2, (TAILLE_FENETRE[1] - 5 * ESPACE_CASE - 6 * TAILLE_CASE)/2 + 25)

DICT_FORCE_REBON = {0 : -2, 1 : -2.5, 2 : -3, 3 : -3.5, 4 : -4.5, 5 : -6, 6 : -8}