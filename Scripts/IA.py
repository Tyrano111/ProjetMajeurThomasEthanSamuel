# Il va s'occuper de gerer toute la partie IA/heuristique du projet (le jeu solo)
#!!! L'IA JOUERA TOUJOURS LES JAUNES !!!

import Game as g
import Main as m

#Valeurs de test

AI_DEPTH=8

test_grid=[ ["j","r","j"," ","j"," ","r"],\
            ["j","j","j"," ","j","r","j"],\
            ["j","r","r","r","r","r","r"],\
            ["r","j","r","j","r","j","r"],\
            ["j","r","j","j","r","r","j"],\
            ["r","j","j","r","j","j","r"]]

#Fonctions de l'IA

def empty_space(grid): #On cherche les collones où on peut placer un jeton (donc les collones où la case du haut est vide)
    empty=[]
    for c in range(len(grid[0])):
        if grid[0][c]==" ":
            empty.append(c)
    return empty

def minimax(grid, player, depth, position): #Par récursivité, on va simuler tous les coups possibles pour l'IA et le joueur, et on va attribuer un score à chaque coup possible (1:L'IA gane, 0: égalité, -1: le joueur gagne)
    other = "r" if player == "j" else "j"
    game_over=m.winner(grid, position, other)
    if game_over[0]: #Si le jeu est terminé, on retourne le score du gagnant
        return 1 if game_over[1]=="j" else -1 #On remplace la couleur du gagnant par un score pour l'IA (1 si l'IA gagne, -1 si le joueur gagne)
    if depth == 0:
        return 0 
    if empty_space(grid)==[]: #Si il n'y a plus de place, on retourne 0 (égalité)
        return 0
    
    values=[]
    for c in empty_space(grid):
        l=m.trouve_position(grid,c,player)[1][0]
        position=(l,c)
        grid[l][c] = player
        if player=="r":
            values.append(minimax(grid, "j", depth - 1, position))
        else: 
            values.append(minimax(grid, "r", depth - 1, position))
        grid[l][c] = " "  

    if player == "j":
        return max(values)  
    return min(values)   

def best_placement(grid): #On cherche le meilleur coup et on renvoit la colonne correspondante
    best_value=None
    best_placement=None

    for c in empty_space(grid): #Optimisation 1: On teste d'abord si l'IA  peut directement gagner en testant chaque colonne
        l=m.trouve_position(grid,c,"j")[1][0]
        grid[l][c] = "j"
        if m.winner(grid, (l,c), "j")[0]:
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    for c in empty_space(grid): #Optimisation 2: On teste ensuite si l'humain peut directement gagner au tour d'après, et on le bloque
        l=m.trouve_position(grid,c,"r")[1][0] 
        grid[l][c] = "r"
        if m.winner(grid, (l,c), "r")[0]:
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    #Optimisation 3: Trouver un chemin qui ne possède que des victoires

    for c in empty_space(grid):
        l=m.trouve_position(grid,c,"j")[1][0]
        grid[l][c] = "j"
        value=minimax(grid, "r", AI_DEPTH, (l,c))
        grid[l][c] = " "
        if best_value==None or value>best_value:
            best_value,best_placement=value,c
        
    return best_placement

#Tests

print(empty_space(test_grid))
print(best_placement(test_grid))