
class Grille:
    def __init__(self):
        self.grille = [[" " for _ in range(7)] for _ in range(6) ]
        self.w_d_haut, self.L_d_haut = False, []
        self.w_d_bas, self.L_d_bas = False, []
        self.w_c, self.L_c = False, []
        self.w_l, self.L_l = False, []

    def trouve_position(self, colonne : int):
        '''Renvoie la position de la case la plus basse de la colonne donnée'''
        if not 0 <= colonne < 7:
            return None
        if self.grille[0][colonne] == ".j" or self.grille[0][colonne] == ".r":
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
        L=[]
        for i in range(7):
            if n < 4:
                if couleur==self.grille[ligne][i]:
                    n=n+1
                    L.append((ligne,i))
                else:
                    n=0
                    L=[]
            elif couleur==self.grille[ligne][i]:
                L.append((ligne,i))
            else:
                return True,L
        if n>=4:
            return True,L
        return False, []

    def gagnant_c(self, position : tuple, couleur : str) -> bool:
        """Vérifie si le dernier coup a permis de gagner sur la colonne"""
        n=0
        L=[]
        colonne=position[1]
        for i in range(6):
            if n < 4:
                if couleur==self.grille[i][colonne]:
                    n=n+1
                    L.append((i,colonne))
                else:
                    n=0
                    L=[]
            elif couleur==self.grille[i][colonne]:
                L.append((i,colonne))
            else:
                return True,L
        if n>=4:
            return True,L
        return False, []

    def position_diagonale_bas(self, position : tuple) -> list:
        '''Renvoie la position de la case la plus basse de la diagonale montante passant par la position donnée'''
        ligne=position[0]
        colonne=position[1]
        deplacement=min(5-ligne,colonne)
        return (ligne + deplacement, colonne - deplacement)

    def position_diagonale_haut(self, position : tuple) -> list:
        '''Renvoie la position de la case la plus haute de la diagonale descendante passant par la position donnée'''
        ligne=position[0]
        colonne=position[1]
        deplacement=min(ligne,colonne)
        return (ligne - deplacement, colonne - deplacement)

    def gagnant_d_bas(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner sur la diagonale montante'''
        position_bas=self.position_diagonale_bas(position)
        ligne=position_bas[0]
        colonne=position_bas[1]
        n=0
        L=[]
        deplacement_min=min(6-colonne,ligne)
        for i in range(deplacement_min+1):
            if n < 4:
                if couleur==self.grille[ligne-i][colonne+i]:
                    n=n+1
                    L.append((ligne-i,colonne+i))
                else:
                    n=0
                    L=[]
            elif couleur==self.grille[ligne-i][colonne+i]:
                L.append((ligne-i,colonne+i))
            else:
                return True,L
        if n>=4:
            return True,L
        return False, []


    def gagnant_d_haut(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner sur la diagonale descendante'''
        position_haut=self.position_diagonale_haut(position)
        ligne=position_haut[0]
        colonne=position_haut[1]
        n=0
        L=[]
        deplacement_min=min(6-colonne,5-ligne)
        for i in range(deplacement_min+1):
            if n < 4:
                if couleur==self.grille[ligne+i][colonne+i]:
                    n=n+1
                    L.append((ligne+i,colonne+i))
                else:
                    n=0
                    L=[]
            elif couleur==self.grille[ligne+i][colonne+i]:
                L.append((ligne+i,colonne+i))
            else:
                return True,L
        if n==4:
            return True,L
        return False, []

    def gagnant_l_IA(self, position : tuple, couleur : str) -> bool:
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

    def gagnant_c_IA(self, position : tuple, couleur : str) -> bool:
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


    def gagnant_d_bas_IA(self, position : tuple, couleur : str) -> bool:
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


    def gagnant_d_haut_IA(self, position : tuple, couleur : str) -> bool:
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

    def winner_IA(self, position : tuple, couleur : str) -> bool:
            '''Vérifie si le dernier coup a permis de gagner'''
            return (self.gagnant_d_haut_IA(position, couleur)
                    or self.gagnant_d_bas_IA(position, couleur)
                    or self.gagnant_c_IA(position, couleur)
                    or self.gagnant_l_IA(position, couleur))

    def annexe_winner(self, position : tuple, couleur : str):
        self.w_d_haut, self.L_d_haut=self.gagnant_d_haut(position, couleur)
        self.w_d_bas, self.L_d_bas=self.gagnant_d_bas(position, couleur)
        self.w_c, self.L_c=self.gagnant_c(position, couleur)
        self.w_l, self.L_l=self.gagnant_l(position, couleur)


    def winner(self, position : tuple, couleur : str) -> bool:
        '''Vérifie si le dernier coup a permis de gagner'''
        self.annexe_winner(position, couleur)
        return (self.w_d_haut
                or self.w_d_bas
                or self.w_c
                or self.w_l)

    def positions_gagnante(self):
        listTot = []
        for elt in self.L_d_haut:
            listTot.append(elt)
        for elt in self.L_d_bas:
            listTot.append(elt)
        for elt in self.L_c:
            listTot.append(elt)
        for elt in self.L_l:
            listTot.append(elt)
        return listTot


    def bloque_colonne(self, colonne : int, couleur : str) -> list:
        '''Bloque la colonne donnée lors de son tour et celui de l'adversaire'''
        if self.compteur_nb_ligne(0) >= 6:
            return False
        couleur_adverse=""
        if couleur=="r":
            couleur_adverse="j"
        else:
            couleur_adverse="r"
        if self.grille[0][colonne] == " " or self.grille[0][colonne] == f".{couleur_adverse}":
            self.grille[0][colonne] = f".{couleur}"
            return True
        return False

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
            if ligne == 5:
                self.grille[ligne][colonne] = couleur
            else:
                self.grille[ligne][colonne]='f'+couleur
            return True, (ligne, colonne)
        return False, None

    def desbloque_fantome(self, position : tuple):
        '''Change le fantôme en jeton classique à la position donnée si il y a un jeton sous le fantôme'''
        ligne=position[0]
        colonne=position[1]
        if ligne==0:
            return None, None
        if self.grille[ligne-1][colonne] == "fr":
            self.grille[ligne-1][colonne] = "r"
            return (ligne-1,colonne), 'r'
        elif self.grille[ligne-1][colonne] == "fj":
            self.grille[ligne-1][colonne] = "j"
            return (ligne-1,colonne), 'j'
        return None, None

    def compteur_nb_ligne(self, indLigne):
        compteur = 0
        for val in self.grille[indLigne]:
            if val != " " and val != ".j" and val != ".r":
                compteur += 1
        return compteur

    def grille_pleine(self):
        compteur = 0
        for i in range(6):
            compteur += self.compteur_nb_ligne(i)
        if compteur == 42:
            return True
        return False