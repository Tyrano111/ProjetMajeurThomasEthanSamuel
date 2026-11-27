from Grille import Grille

class Jeu:
    def __init__(self):
        self.grille = Grille()

        self.joueur = "r"

        self.etat = "Accueil" 
        self.echap = False

        self.sorts = {
            "r": ["Normal", "Normal", "Normal"],
            "j": ["Normal", "Normal", "Normal"]
        }

        self.compteursSortBloqueLigne = {"r": 0, "j": 0}
        self.jetonNoir = False
        self.sortUtilise = False
        self.sortConso = False

    def ChangerJoueur(self):
        """changement de joueur"""
        self.joueur = "r" if self.joueur == "j" else "j"

    def JouerCoup(self, colonne):
        position = self.grille.place_jeton(colonne, self.joueur)
        if position is None:
            return None
        if self.etat == "Solo":
            liste = self.TerminerTourSolo(position)
        else:
            liste = self.TerminerTourJcj(position)
        return liste

    def TerminerTourJcj(self, position):
        for cle in self.compteursSortBloqueLigne:
            if self.compteursSortBloqueLigne[cle] > 0:
                self.compteursSortBloqueLigne[cle] -= 1

            if self.compteursSortBloqueLigne[cle] == 0 or self.grille.compteur_nb_ligne(0) == 6:
                self.grille.desbloque_colonne(cle)
        self.sortConso = False
        if self.jetonNoir:
            self.jetonNoir = False
        if not self.sortUtilise:
            posFantome, couleurFantome = self.grille.desbloque_fantome(position)
            
            while posFantome is not None:
                verif = self.VerificationVictoire(posFantome, couleurFantome)
                if verif:
                    self.joueur = couleurFantome
                elif self.grille.grille_pleine():
                    self.etat = "Egalite"
                posFantome, couleurFantome = self.grille.desbloque_fantome(posFantome)
                if verif:
                    return self.grille.positions_gagnante()
        verif = self.VerificationVictoire(position, self.joueur)
        if verif:
            return self.grille.positions_gagnante()
        elif self.grille.grille_pleine():
            self.etat = "Egalite"
        else:
            self.ChangerJoueur()
        return None

    def TerminerTourSolo(self, position):
            verif = self.VerificationVictoire(position, self.joueur)
            if verif:
                return self.grille.positions_gagnante()
            elif self.grille.grille_pleine():
                self.etat = "Egalite"
            else:
                self.ChangerJoueur()
                return None

    def VerificationVictoire(self, position, couleur):
        return self.grille.winner(position, couleur)

    def SortBloqueColonne(self, colonne):
        peutUtilise = self.grille.bloque_colonne(colonne, self.joueur)
        if peutUtilise:
            self.compteursSortBloqueLigne[self.joueur] = 2
            self.sorts[self.joueur][0] = "Utilise"
            return True
        self.sorts[self.joueur][0] = "Normal"
        return False

    def SortJetonNoir(self, colonne):
        position = self.grille.place_jeton(colonne, "n")
        if position is None:
            return None
        self.jetonNoir = False
        self.sorts[self.joueur][1] = "Utilise"
        posFantome, couleurFantome = self.grille.desbloque_fantome(position)
        while posFantome is not None:
            verif = self.VerificationVictoire(posFantome, couleurFantome)
            if verif:
                self.joueur = couleurFantome
            elif self.grille.grille_pleine():
                self.etat = "Egalite"
            posFantome, couleurFantome = self.grille.desbloque_fantome(posFantome)
            if verif:
                return self.grille.positions_gagnante()
            
        return None

    def SortFantome(self, position):
        self.sortUtilise, posFantome = self.grille.fantome(position, self.joueur)
        if self.sortUtilise:
            self.sorts[self.joueur][2] = "Utilise"
            if posFantome[0] != 5:
                posSousFantome = (posFantome[0] + 1, posFantome[1])
                if self.grille.grille[posSousFantome[0]][posSousFantome[1]] == "j" or self.grille.grille[posSousFantome[0]][posSousFantome[1]] == "r" or self.grille.grille[posSousFantome[0]][posSousFantome[1]] == "n":
                    posFantome, couleurFantome = self.grille.desbloque_fantome(posSousFantome)
                    while posFantome is not None:
                        verif = self.VerificationVictoire(posFantome, couleurFantome)
                        if verif:
                            self.joueur = couleurFantome
                        elif self.grille.grille_pleine():
                            self.etat = "Egalite"
                        posFantome, couleurFantome = self.grille.desbloque_fantome(posFantome)
                        if verif:
                            return True, self.grille.positions_gagnante()
            else:
                self.sortUtilise = False
            self.TerminerTourJcj(position)
            return True, None
        return False, None


    def ReinitialiserPartie(self):
        self.grille.reinitialisation_grille()
        self.sorts = {
            "r": ["Normal", "Normal", "Normal"],
            "j": ["Normal", "Normal", "Normal"]
        }
        self.joueur = "r"
        self.etat = "Accueil"
        self.echap = False
        self.compteursSortBloqueLigne = {"r": 0, "j": 0}
        self.jetonNoir = False
        self.sortUtilise = False
        self.sortConso = False

    def changerEtat(self, prochainEtat):
        self.etat = prochainEtat

    def SelectionnerEtatSort(self, prochainEtat, ind):
        self.sorts[self.joueur][ind] = prochainEtat

    
    