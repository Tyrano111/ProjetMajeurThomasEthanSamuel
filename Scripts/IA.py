# Il va s'occuper de gerer toute la partie IA/heuristique du projet (le jeu solo)
#!!! L'IA JOUERA TOUJOURS LES JAUNES (pour laisser plus de chance au joueur)!!!

from copy import deepcopy
import ConstantesEtVariable as cv

#Fonctions de l'IA

def empty_space(grid): #On cherche les colonnes où on peut placer un jeton (donc les colonnes où la case du haut est vide)
    empty=[]
    for c in range(len(grid[0])):
        if grid[0][c]==" ":
            empty.append(c)
    empty.sort(key=lambda x: abs(x-3)) #On trie les colonnes par rapport à la colonne centrale (la plus centrale est la meilleure)
    return empty

def score_grid(grid): #Score entre 0.9 et -0.9, toujours entre une défaite (-1) et une victoire (1), source: IA
    score = 0
    for fenetre in cv.FENETRES:
        j = 0
        r = 0
        for (l, c) in fenetre:
            if grid[l][c] == "j":
                j += 1
            elif grid[l][c] == "r":
                r += 1
        if j!=0 and r!=0: #La fenêtre est composée des 2 ou d'aucune des 2 couleurs, inutile pour les deux camps
            continue
        if j!=0:
            score += cv.POIDS[("j", j)]
        elif r!=0:
            score += cv.POIDS[("r", r)]
    return 0.9 * score / (abs(score) + 60) #Permet de borner le score entre -0.9 et 0.9 (+60 valeur arbitraire déterminée par IA en testant plusieurs parties)

def minimax(grid_object, player, depth, position, alpha, beta): #Par récursivité, on va simuler tous les coups possibles pour l'IA et le joueur, et on va attribuer un score à chaque coup possible (1:L'IA gane, 0: égalité, -1: le joueur gagne)
    grid = grid_object.grille
    other = "r" if player == "j" else "j"
    game_over=grid_object.winner(position, other)
    if game_over: #Si le jeu est terminé, on retourne le score du gagnant
        return (1+depth/1000) if other=="j" else (-1-depth/1000) #On remplace la couleur du gagnant par un score pour l'IA (1 si l'IA gagne, -1 si le joueur gagne), on ajoute depth/1000 pour favoriser les victoires rapides et les défaites lentes
    if depth == 0: #Si on a atteint la profondeur maximale, on retourne 0 (on se sait pas)
        return score_grid(grid)
    if empty_space(grid)==[]: #Si il n'y a plus de place, on retourne 0 (égalité)
        return 0

    best_value=-2 if player=="j" else 2 #On initialise le meilleur score à -2 (plus petit que toutes les valeurs) si c'est le tour de l'IA, et à 2 (plus grand que toutes les valeurs) si c'est le tour du joueur
    
    for c in empty_space(grid):
        
        l=grid_object.trouve_position(c)[0]
        position=(l,c)
        grid[l][c] = player
        value=(minimax(grid_object, other, depth - 1, position, alpha, beta))
        grid[l][c] = " "  

        if player=="j":
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)      #On a au moins ça
        else:
            best_value = min(best_value, value)
            beta = min(beta, best_value)        #On a au plus ça

        if alpha >= beta:                       #Cette branche ne peut pas changer la décision, on la retire
            break

    return best_value

def best_placement(grid_object): #On cherche le meilleur coup pour l'IA et on renvoit la colonne correspondante
    grid = grid_object.grille
    best_value=None
    best=None
    a_explorer=empty_space(grid)

    for c in a_explorer: #Optimisation 1: On teste d'abord si l'IA  peut directement gagner en testant chaque colonne
        l=grid_object.trouve_position(c)[0]
        grid[l][c] = "j"
        if grid_object.winner((l,c), "j"):
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    for c in a_explorer: #Optimisation 2: On teste ensuite si l'humain peut directement gagner au tour d'après, et on le bloque
        l=grid_object.trouve_position(c)[0]
        grid[l][c] = "r"
        if grid_object.winner((l,c), "r"):
            grid[l][c] = " "
            return c
        grid[l][c] = " "
    #Optimisation 3: Jouer au centre en priorité (voir empty_space())
    #Opitmisation 4: Alpha beta pruning (on ne teste pas les coups qui sont moins bons que ceux déjà testés) Source: https://www.geeksforgeeks.org/dsa/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    #Opimisation 5: Au lieu de renvoyer 0 si on ne sait pas, on renvoie le score (voir score_grid())
    for c in a_explorer:
        l=grid_object.trouve_position(c)[0]
        grid[l][c] = "j"
        value=minimax(grid_object, "r", cv.AI_DEPTH, (l,c), -2,2)
        grid[l][c] = " "
        if best_value==None or value>best_value:
            best_value,best=value,c
        
    return best