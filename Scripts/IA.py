# Il va s'occuper de gerer toute la partie IA/heuristique du projet (le jeu solo)

import Game as g

AI_DEPTH=20

empty_grid=[["","","","","","",""],\
            ["","","","","","",""],\
            ["","","","","","",""],\
            ["","","","","","",""],\
            ["","","","","","",""],\
            ["","","","","","",""]]

def empty_space(grid):
    empty=[]
    for c in range(len(grid[0])):
        if grid[0][c]=="":
            empty.append(c)
    return empty

def winner(grid):
    return 1 if g.gagnant(grid)=="j" else -1

def minimax(grid, player, depth):
    if g.game_over(grid):
        return winner(grid)
    if depth == 0:
        return 0 
    values = []

    for c in empty_space(grid):
        pos_l=g.position(c,player)[1][0]
        grid[pos_l][c]=player
        if player=="r":
            values.append(minimax(grid, "j", depth - 1))
        else: 
            values.append(minimax(grid, "r", depth - 1))
        grid[pos_l][c] = ""  

    if player == "r":
        return max(values)  
    return min(values)   

def best_placement(grid):
    grid=grid[:]
    best_value=None
    best_placement=None

    for c in empty_space(grid):
        pos_l=g.position(c,"r")[1][0]
        grid[pos_l][c]="r"
        value=minimax(grid, "r", AI_DEPTH)
        grid[pos_l][c]=""
        if best_value==None:
            best_value,best_placement=value,c
        elif value>best_value:
            best_value,best_placement=value,c

    return best_placement

print(empty_space(empty_grid))
print(minimax(empty_grid, "r", AI_DEPTH))