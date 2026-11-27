from Grille import Grille

class Jeu:
    """Class permettant de creer un objet Jeu qui s'occupe de toute la partie fonctionnel du jeu"""
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

    def JouerCoup(self, colonne: int):
        """permet de lancer le placement du jeton et la fin du tour"""
        position = self.grille.place_jeton(colonne, self.joueur)
        if position is None:
            return None
        if self.etat == "Solo":
            liste = self.TerminerTourSolo(position)
        else:
            liste = self.TerminerTourJcj(position)
        return liste

    def TerminerTourJcj(self, position: tuple[int, int]):
        """permet d'effectuer toutes les actions de fin de tour. Ici changer de joueur, modifier les variables de sort et verifier si un joueur a gagné"""
        for cle in self.compteursSortBloqueLigne:
            if self.compteursSortBloqueLigne[cle] > 0:
                self.compteursSortBloqueLigne[cle] -= 1

            if self.compteursSortBloqueLigne[cle] == 0 or self.grille.compteur_nb_ligne(0) == 6:
                self.grille.desbloque_colonne(cle)
        self.sortConso = False
        if self.jetonNoir:
            self.jetonNoir = False
        verif = self.VerificationVictoire(position, self.joueur)
        if verif:
            self.VerificationVictoireFantome(position)
            return self.grille.positions_gagnante()
        elif self.grille.grille_pleine():
            self.etat = "Egalite"
        else:
            self.ChangerJoueur()
        self.VerificationVictoireFantome(position)
        return None

    def TerminerTourSolo(self, position: tuple[int, int]):
            """fonction fait pour le mode solo qui lance dle changement du joueur et la verification de la victoire d'un joueur"""
            verif = self.VerificationVictoire(position, self.joueur)
            if verif:
                return self.grille.positions_gagnante()
            elif self.grille.grille_pleine():
                self.etat = "Egalite"
            else:
                self.ChangerJoueur()
                return None

    def VerificationVictoire(self, position: tuple[int, int], couleur: str)-> bool:
        """fonction qui lance la verification de victoire"""
        return self.grille.winner(position, couleur)

    def SortBloqueColonne(self, colonne: int)-> bool:
        """fonction permettant d'actionner le lancement du sort qui bloque une colonne"""
        peutUtilise = self.grille.bloque_colonne(colonne, self.joueur)
        if peutUtilise:
            self.compteursSortBloqueLigne[self.joueur] = 2
            self.sorts[self.joueur][0] = "Utilise"
            return True
        self.sorts[self.joueur][0] = "Normal"
        return False

    def SortJetonNoir(self, colonne:int):
        """fonction permettant d'actionner le lancement du sort qui pose un jeton noir"""
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
        return

    def SortFantome(self, position:tuple[int, int])-> tuple:
        """fonction permettant d'actionner le lancement du sort qui place un jeton fantome"""
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
                            return True, self.grille.positions_gagnante()
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


    def ReinitialiserPartie(self)-> None:
        """fonction reinitialisant toute les variables venant de jeu"""
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

    def changerEtat(self, prochainEtat: str)-> None:
        """permet de changer l'etat actuel du jeu"""
        self.etat = prochainEtat

    def SelectionnerEtatSort(self, prochainEtat: str, ind: int)->None:
        """permet de changer l'etat d'un sort"""
        self.sorts[self.joueur][ind] = prochainEtat

    def VerificationVictoireFantome(self, position: tuple[int, int])-> None:
        if not self.sortUtilise:
            posFantome, couleurFantome = self.grille.desbloque_fantome(position)
            while posFantome is not None:
                verif = self.VerificationVictoire(posFantome, couleurFantome)
                if verif:
                    self.joueur = couleurFantome
                elif self.grille.grille_pleine():
                    self.etat = "Egalite"
                posFantome, couleurFantome = self.grille.desbloque_fantome(posFantome)