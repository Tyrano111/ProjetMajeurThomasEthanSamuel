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
        self.joueur = "r" if self.joueur == "j" else "j"

    def JouerCoup(self, colonne):
        position = self.grille.place_jeton(colonne, self.joueur)
        if position is None:
            return False

        if self.etat == "Solo":
            self.TerminerTourSolo(position)
        else:
            self.TerminerTourJcj(position)
        return True

    def TerminerTourJcj(self, position):
        for cle in self.compteursSortBloqueLigne:
            if self.compteursSortBloqueLigne[cle] > 0:
                self.compteursSortBloqueLigne[cle] -= 1

            if self.compteursSortBloqueLigne[cle] == 0:
                self.grille.desbloque_colonne(cle)
        self.sortConso = False
        if self.jetonNoir:
            self.jetonNoir = False
        if self.VerificationVictoire(position, self.joueur):
            self.etat = "Victoire"
        else:
            self.ChangerJoueur()
        posFantome, couleurFantome = self.grille.desbloque_fantome(position)
        while posFantome is not None:
            if self.VerificationVictoire(posFantome, couleurFantome):
                self.joueur = couleurFantome
                self.etat = "Victoire"
            posFantome, couleurFantome = self.grille.desbloque_fantome(posFantome)

    def TerminerTourSolo(self, position):
            if self.VerificationVictoire(position, self.joueur):
                self.etat = "Victoire"
            else:
                self.ChangerJoueur()

    def VerificationVictoire(self, position, couleur):
        return self.grille.winner(position, couleur)

    def SortBloqueColonne(self, colonne):
        self.grille.bloque_colonne(colonne, self.joueur)
        self.compteursSortBloqueLigne[self.joueur] = 2
        self.sorts[self.joueur][0] = "Utilise"

    def SortJetonNoir(self, colonne):
        position = self.grille.place_jeton(colonne, "n")
        if position is None:
            return False
        self.jetonNoir = False
        self.sorts[self.joueur][1] = "Utilise"
        return True

    def SortFantome(self, position):

        self.grille.fantome(position, self.joueur)
        self.sorts[self.joueur][2] = "Utilise"
        self.TerminerTourJcj(position)


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