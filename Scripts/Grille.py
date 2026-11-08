
class Grille:
    def __init__(self):
        self.grille = [[" " for _ in range(7)] for _ in range(6) ]

    def trouve_position(self, colonne : int):
        '''Renvoie la position de la case la plus basse de la colonne donnée'''
        if not 0 <= colonne < 7:
            return None
        if self.grille[0][colonne] != " ":
            return None
        
        for ligne in range(5, -1, -1):
            if self.grille[ligne][colonne] == " ":
                return ligne, colonne
        return None

    def place_jeton(self, colonne : int, couleur : str):
        position = self.trouve_position(colonne)
        if position is None:
            return None

        self.grille[position[0]][position[1]] = couleur
        return position

    def reinitialisation_grille(self):
        self.grille = [[" " for _ in range(7)] for _ in range(6) ]
    
    def gagnant_l(self, position : tuple, couleur : str) -> bool:
        """Vérifie si le dernier coup a permis de gagner sur la ligne"""
        ligne=position[0]
        n=0
        for i in range(7):
            if couleur==self.grille[ligne][i]:
                n=n+1
            else:
                n=0
            if n==4:
                return True
        return False

    def gagnant_c(self, position : tuple, couleur : str) -> bool:
        """Vérifie si le dernier coup a permis de gagner sur la colonne"""
        n=0
        colonne=position[1]
        for i in range(6):
            if couleur==self.grille[i][colonne]:
                n=n+1
            else:
                n=0
            if n==4:
                return True
        return False

    def position_diagonale_bas(self, position : tuple) -> list:
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

    def position_diagonale_haut(self, position : tuple) -> list:
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

    def gagnant_d_bas(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner sur la diagonale montante'''
        position_bas=self.position_diagonale_bas(position)
        ligne=position_bas[0]
        colonne=position_bas[1]
        n=0
        deplacement_min=min(6-colonne,ligne)
        for i in range(deplacement_min+1):
            if couleur==self.grille[ligne-i][colonne+i]:
                n=n+1
            else:
                n=0
            if n==4:
                return True
        return False  


    def gagnant_d_haut(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner sur la diagonale descendante'''
        position_haut=self.position_diagonale_haut(position)
        ligne=position_haut[0]
        colonne=position_haut[1]
        n=0
        deplacement_min=min(6-colonne,5-ligne)
        for i in range(deplacement_min+1):
            if couleur==self.grille[ligne+i][colonne+i]:
                n=n+1
            else:
                n=0
            if n==4:
                return True
        return False  


    def winner(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner'''
        return (self.gagnant_d_haut(position, couleur)
                or self.gagnant_d_bas(position, couleur)
                or self.gagnant_c(position, couleur)
                or self.gagnant_l(position, couleur))

    def bloque_colonne(self, colonne : int, couleur : str) -> list:
        '''Bloque la colonne donnée lors de son tour et celui de l'adversaire'''
        couleur_adverse=""
        if couleur=="r":
            couleur_adverse="j"
        else:
            couleur_adverse="r"
        if self.grille[0][colonne] == " " or self.grille[0][colonne] == f".{couleur_adverse}":
            self.grille[0][colonne] = f".{couleur}"
        return self.grille

    def desbloque_colonne(self, couleur : str) -> list:
        '''Débloque la colonne bloquée lors de son tour précédant'''
        for i in range(7):
            if self.grille[0][i]== f".{couleur}":
                self.grille[0][i]= " " 

    def fantome(self, position : tuple, couleur : str):
        '''Place un fantôme de la couleur donnée à la position donnée'''
        ligne=position[0]
        colonne=position[1]
        if self.grille[ligne][colonne]==" "  and self.grille[0][colonne]!='.r' and self.grille[0][colonne]!='.j':
            self.grille[ligne][colonne]='f'+couleur

    def desbloque_fantome(self, position : tuple):
        '''Change le fantôme en jeton classique à la position donnée si il y a un jeton sous le fantôme'''
        ligne=position[0]
        colonne=position[1]
        if ligne==0:
            return None, None
        if self.grille[ligne-1][colonne]=="fr":
            self.grille[ligne-1][colonne]= "r"
            return (ligne-1,colonne), 'r'
        elif self.grille[ligne-1][colonne]== "fj":
            self.grille[ligne-1][colonne]= "j"
            return (ligne-1,colonne), 'j'
        return None, None