# Il va s'occuper de gerer toute la partie IA/heuristique du projet (le jeu solo)

import Game as g
import Main as m

#Valeurs de test

AI_DEPTH=5

test_grid=[ [" "," "," "," "," "," ","j"],\
            [" "," "," "," "," "," ","r"],\
            [" "," "," "," "," "," ","j"],\
            [" "," "," "," ","r"," ","r"],\
            [" "," "," ","j","r","r","j"],\
            [" "," "," ","j","j","j","r"]]

#Fonctions de l'IA

def empty_space(grid): #On cherche les colonnes où on peut placer un jeton (donc les colonnes où la case du haut est vide)
    empty=[]
    for c in range(len(grid[0])):
        if grid[0][c]==" ":
            empty.append(c)
    return empty

def minimax(grid, player, depth, position): #Par récursivité, on va simuler tous les coups possibles pour l'IA et le joueur, et on va attribuer un score à chaque coup possible (1:L'IA gane, 0: égalité, -1: le joueur gagne)
    game_over=m.winner(grid, position, player)
    if game_over[0]: #Si le jeu est terminé, on retourne le score du gagnant
        print("game_over:",position, game_over[1])
        m.afficher(grid)
        return 1 if game_over[1]=="j" else -1 #On remplace la couleur du gagnant par un score pour l'IA (1 si l'IA gagne, -1 si le joueur gagne)
    if depth == 0:
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

def best_placement(grid):
    grid=grid[:]
    best_value=None
    best_placement=None

    for c in empty_space(grid):
        l=m.trouve_position(grid,c,"j")[1][0]
        grid[l][c] = "j"
        value=minimax(grid, "j", AI_DEPTH, (l,c))
        grid[l][c] = " "
        if best_value==None:
            best_value,best_placement=value,c
        elif value>best_value:
            best_value,best_placement=value,c
        
    return best_placement

#Tests

print(empty_space(test_grid))
#print(minimax(test_grid, "j", AI_DEPTH, (0,0)))
print(best_placement(test_grid))