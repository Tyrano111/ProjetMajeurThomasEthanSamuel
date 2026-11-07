# Il va s'occuper de gerer toute la partie IA/heuristique du projet (le jeu solo)
#!!! L'IA JOUERA TOUJOURS LES JAUNES (pour laisser plus de chance au joueur)!!!

import Game as g

#Valeurs de test

AI_DEPTH=10

empty_grid=[[" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "]]

test_grid=[ [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," "," "," "," "," "],\
            [" "," "," ","r"," "," "," "]]

#Fonctions de l'IA

def empty_space(grid): #On cherche les colonnes où on peut placer un jeton (donc les colonnes où la case du haut est vide)
    empty=[]
    for c in range(len(grid[0])):
        if grid[0][c]==" ":
            empty.append(c)
    empty.sort(key=lambda x: abs(x-3)) #On trie les colonnes par rapport à la colonne centrale (la plus centrale est la meilleure)
    return empty

def minimax(grid, player, depth, position, couleur, alpha=-2, beta=2): #Par récursivité, on va simuler tous les coups possibles pour l'IA et le joueur, et on va attribuer un score à chaque coup possible (1:L'IA gane, 0: égalité, -1: le joueur gagne)
    other = "r" if player == "j" else "j"
    game_over=g.winner(position, other)
    if game_over: #Si le jeu est terminé, on retourne le score du gagnant
        return 1 if other=="j" else -1 #On remplace la couleur du gagnant par un score pour l'IA (1 si l'IA gagne, -1 si le joueur gagne)
    if depth == 0: #Si on a atteint la profondeur maximale, on retourne 0 (on se sait pas)
        return 0 
    if empty_space(grid)==[]: #Si il n'y a plus de place, on retourne 0 (égalité)
        return 0

    best_value=-2 if player=="j" else 2 #On initialise le meilleur score à -2 (plus petit que toutes les valeurs) si c'est le tour de l'IA, et à 2 (plus grand que toutes les valeurs) si c'est le tour du joueur
    
    for c in empty_space(grid):
        l=g.trouve_position(c, couleur)[1]
        position=(l,c)
        grid[l][c] = player
        value=(minimax(grid, other, depth - 1, position, couleur, alpha, beta))
        grid[l][c] = " "  

        if player=="j":
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)      # on a au moins ça
        else:
            best_value = min(best_value, value)
            beta = min(beta, best_value)        # on a au plus ça

        if (player == "j" and best_value == 1) or (player == "r" and best_value == -1):
            break

    
    return best_value

def best_placement(grid, couleur): #On cherche le meilleur coup pour l'IA et on renvoit la colonne correspondante
    best_value=None
    best=None
    a_explorer=empty_space(grid)

    for c in a_explorer: #Optimisation 1: On teste d'abord si l'IA  peut directement gagner en testant chaque colonne
        l=g.trouve_position(c, couleur)[1]
        grid[l][c] = "j"
        if g.winner((l,c), "j"):
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    for c in a_explorer: #Optimisation 2: On teste ensuite si l'humain peut directement gagner au tour d'après, et on le bloque
        l=g.trouve_position(c, couleur)[1]
        grid[l][c] = "r"
        if g.winner((l,c), "r"):
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    #Optimisation 3: Jouer au centre en priorité (voir empty_space() )
    #Opitmisation 4: Alpha beta pruning (on ne teste pas les coups qui sont moins bons que ceux déjà testés) Source: https://www.youtube.com/watch?v=l-hh51ncgDI
    for c in a_explorer:
        l=g.trouve_position(c, couleur)[1]
        grid[l][c] = "j"
        value=minimax(grid, "r", AI_DEPTH, (l,c), couleur, -2,2)
        grid[l][c] = " "
        if best_value==None or value>best_value:
            best_value,best=value,c
        
    return best

#Tests
