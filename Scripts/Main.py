import pygame
import threading
import copy
from Jeu import Jeu
import ConstantesEtVariable as CV
import UI
import IA


class Main:
    def __init__(self):
        #Activation de pygame et lancement du jeu
        pygame.init()
        self.ecran = pygame.display.set_mode(CV.TAILLE_FENETRE)
        pygame.display.set_caption("Puissance 4.5")
        self.__clock = pygame.time.Clock()
        self.__jeu = Jeu()

        #Ui :
        self.__accueil = UI.Accueil()
        self.__uiPause = UI.Pause()
        self.__uiGrille = UI.AffichageGrille()
        self.__jeton = UI.Jeton()
        self.__boutons = {
            "r" : [UI.BoutonSort((1050, 175), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 375), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 575), 128, "Assets/BoutonFantome")], 
            "j" : [UI.BoutonSort((1050, 175), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 375), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 575), 128, "Assets/BoutonFantome")]
            }
        self.__victoire = UI.Victoire()

        #Variables pour le placement des jetons et le bon deroulement du tour
        self.__estEnChute = False
        self.__indiceFuturPosition = (0, 0)
        self.__positionFuturJeton = (0, 0)
        self.__forceRebon = 0

        #Variables Ia
        self.__tourIa = False
        self.__threadIa = None        # thread de calcul en cours (None = aucun)
        self.__resultatIa = None      # colonne choisie, None tant que le calcul n'est pas fini
        self.__numeroPartie = 0       # permet d'ignorer un vieux calcul après une réinitialisation
        self.fontIa = pygame.font.SysFont("Corbel", 30)

        #Variable pour les sorts
        self.__indSortEnCour = 0
        self.__boutonFantomeActif = False

        #Varible pour les particules
        self.__listePosGagnante = None
        self.__particules = []
        self.__dt = None
        self.__puissanceMax = False
        

    def Update(self)-> None:
        """fonction qui gére tout le jeu. Elle change les ecrans au bon moment et s'occupe de la base de pygame"""
        while self.__jeu.etat != "":
            self.ecran.fill("black")
            self.__dt = self.__clock.tick(60) / 500
            if self.__jeu.etat == "Accueil":
                self.UpdateAccueil()
            elif self.__jeu.etat == "Victoire" or self.__jeu.etat == "Egalite":
                self.UpdateVictoire()
            else:
                if self.__jeu.echap:
                    self.UpdatePause()
                elif self.__jeu.etat == "Solo":
                    self.UpdateSolo()
                else:
                    self.UpdateJcj()
                
            pygame.display.flip()
        pygame.quit()


    def UpdateAccueil(self)-> None:
        """fonction qui s'occupe de l'accueil, elle l'affiche et permet de faire les action à l'interieur"""
        self.__accueil.draw(self.ecran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.__accueil.BoutonClique(mouse)
                if clique != 0:
                    if clique == 1:
                        self.__jeu.etat = "Solo"
                    elif clique == 2:
                        self.__jeu.etat = "Jcj"
                    else:
                        self.__jeu.etat = ""


    def UpdateSolo(self)-> None:
        """fonction qui s'occupe du mode solo, elle l'affiche et permet de faire les action à l'interieur"""
        self.PlacementJeton()
        self.Interfacejeu()
        if self.__listePosGagnante is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__jeu.etat = "" 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__jeu.echap = True
                elif not self.__estEnChute and not self.__tourIa:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()
                            resultatPosition = self.EmplacementSourieGrille(mouse)
                            if resultatPosition[0]:
                                self.ActivationVariableDePlacement(resultatPosition[1][1])
            if self.__tourIa and not self.__estEnChute:
                if self.__threadIa is None:
                    # Lancement du calcul sur une copie de la grille
                    copieGrille = copy.deepcopy(self.__jeu.grille)
                    self.__threadIa = threading.Thread(
                        target=self.CalculerCoupIa,
                        args=(copieGrille, self.__numeroPartie),
                        daemon=True)
                    self.__threadIa.start()
                elif self.__resultatIa is not None:
                    # Le calcul est terminé : on joue le coup
                    self.ActivationVariableDePlacement(self.__resultatIa)
                    self.__threadIa = None
                    self.__resultatIa = None
                else:
                    # Calcul en cours : on affiche un message
                    texte = self.fontIa.render("L'IA réfléchit...", True, (217, 217, 217))
                    self.ecran.blit(texte, (1115, 760))
        else:
            self.GererAvantVictoire()
        
        

    def UpdateJcj(self)-> None:
        """fonction qui s'occupe du mode joueur contre joueur, elle l'affiche et permet de faire les action à l'interieur"""
        self.PlacementJeton()
        self.Interfacejeu()
        if self.__listePosGagnante is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__jeu.etat = "" 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__jeu.echap = True
                elif not self.__estEnChute:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()
                            resultatPosition = self.EmplacementSourieGrille(mouse)
                            if resultatPosition[0]:
                                if not self.__jeu.sortConso:
                                      self.UtilisationSort(resultatPosition)
                                if not self.__jeu.sortUtilise:
                                    self.ActivationVariableDePlacement(resultatPosition[1][1])
                            elif not self.__jeu.sortConso:
                                etatSortJoueur = self.__jeu.sorts[self.__jeu.joueur]
                                for ind, bouton in enumerate(self.__boutons[self.__jeu.joueur]):
                                    if etatSortJoueur[ind] != "Utilise":
                                        if bouton.est_clique(mouse) and etatSortJoueur[ind] == "Normal":
                                            if self.__indSortEnCour != ind and etatSortJoueur[self.__indSortEnCour] == "Clique":
                                                self.__jeu.SelectionnerEtatSort("Normal", self.__indSortEnCour)
                                                self.__indSortEnCour = ind
                                            self.__jeu.SelectionnerEtatSort("Clique", ind)
                                            self.__indSortEnCour = ind
                                            if ind == 2:
                                                self.__boutonFantomeActif = True
                                            else:
                                                self.__boutonFantomeActif = False
                                        elif bouton.est_clique(mouse) and etatSortJoueur[ind] == "Clique":
                                            self.__jeu.SelectionnerEtatSort("Normal", ind)
                                            
                                            self.__boutonFantomeActif = False
        else:
            self.GererAvantVictoire()
                                
        

    def UpdatePause(self)-> None:
        """fonction qui s'occupe du menu de pause, elle l'affiche et permet de faire les action à l'interieur"""
        self.Interfacejeu()
        self.__uiPause.draw(self.ecran)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.__uiPause.BoutonClique(mouse)
                if clique == 1:
                    self.__jeu.echap = False
                if clique == 2:
                    self.ReinitialiserJeu()

    def UpdateVictoire(self)-> None:
        """fonction qui s'occupe du menu de victoire, elle l'affiche et permet de faire les action à l'interieur"""
        self.__victoire.draw(self.ecran, self.__jeu.joueur, self.__jeu.etat)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.__victoire.boutonMenu.est_clique(mouse):
                    self.ReinitialiserJeu()

    def ReinitialiserJeu(self)-> None:
        """fonction qui reinitilise toutes les variables du jeu pour pouvoir en relancer une sans être affecté par les autres"""
        self.__jeu.ReinitialiserPartie()
        self.__jeton.ReinitialiserJeton()
        self.__tourIa = False
        self.__estEnChute = False
        self.__boutonFantomeActif = False
        self.__indSortEnCour = 0
        self.__particules = []
        self.__puissanceMax = False
        self.__listePosGagnante = None
        self.__numeroPartie += 1
        self.__threadIa = None
        self.__resultatIa = None

    def Interfacejeu(self)-> None:
        """fonction qui affiche tout l'ecran de jeu, elle affiche la grille et les boutons de sort"""
        mouse = pygame.mouse.get_pos()
        self.__uiGrille.draw(self.__jeu.grille.grille, self.ecran, mouse, self.__boutonFantomeActif, self.__jeu.joueur)
        if self.__jeu.etat != "Solo":
            for i in range(len(self.__boutons[self.__jeu.joueur])):
                self.__boutons[self.__jeu.joueur][i].draw(self.ecran, self.__jeu.sorts[self.__jeu.joueur][i])

    def EmplacementSourieGrille(self, mouse: tuple[float, float])-> tuple:
        """fonction permettant de savoir ou se situe la sourie sur la grille. Elle renvoie un tuple avec est ce que la sourie est dans la grille et sa position"""
        for indLigne, ligne in enumerate(self.__jeu.grille.grille):
            posLigne = CV.POS_GRILLE_Y + indLigne * CV.TAILLE_CASE
            for indColonne in range(len(ligne)):
                posColone = CV.POS_GRILLE_X + indColonne * CV.TAILLE_CASE
                rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    return True, (indLigne, indColonne)
        return False, None

    def TransformationIndiceEnPositon(self, indice: tuple[int, int])-> tuple[float, float]:
        """fonction qui transforme un indice de grille en position"""
        return CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE, CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE

    def TransformationIndiceEnPositonParticule(self, indice: tuple[int, int])-> tuple[float, float]:
        """fonction qui transforme un indice de grille en position pour le placer au millieu d'un jeton"""
        return (
            CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE + CV.TAILLE_CASE // 2,
            CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE + CV.TAILLE_CASE // 2
        )

    def PlacementJeton(self)-> None:
        """fonction pour faire les actions du jeu.
        elle permet de poser un jeton ou de jouer un sort"""
        if self.__estEnChute:
            self.__forceRebon = self.__jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, "n") if self.__jeu.jetonNoir else self.__jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, self.__jeu.joueur)
            if self.__forceRebon == 0:
                if self.__jeu.etat == "Solo":
                    self.__tourIa = False if self.__tourIa else True
                if self.__jeu.jetonNoir:
                    self.__listePosGagnante = self.__jeu.SortJetonNoir(self.__indiceFuturPosition[1])
                else:
                    self.__listePosGagnante = self.__jeu.JouerCoup(self.__indiceFuturPosition[1])
                self.CreerParticules()
                self.__estEnChute = False
                self.__jeton.position[1] = 0
        if self.__jeu.sortUtilise:
            self.__jeu.sortUtilise = False

    def ActivationVariableDePlacement(self, indcolonne: int)-> None:
        """fonction permettant de lancer le placement du jeton"""
        self.__indiceFuturPosition = indcolonne
        self.__indiceFuturPosition = self.__jeu.grille.trouve_position(indcolonne)
        if self.__indiceFuturPosition is not None:
            self.__estEnChute = True
            self.__positionFuturJeton = self.TransformationIndiceEnPositon(self.__indiceFuturPosition)
            self.__forceRebon = CV.DICT_FORCE_REBON[self.__indiceFuturPosition[0]]


    def CreerParticules(self)-> None:
        """fonction creant les particules en cas de victoire"""
        if self.__listePosGagnante is not None:
            if len(self.__listePosGagnante) >= 5:
                self.__puissanceMax = True
            self.__particules = []
            for ind in self.__listePosGagnante:
                position = self.TransformationIndiceEnPositonParticule(ind)
                particule = UI.Particule(position, 300, self.__jeu.joueur, self.__puissanceMax)
                self.__particules.append(particule)

    def GererAvantVictoire(self)-> None:
        """fonction qui s'occupe du fonctionnement d'avant victoire"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__jeu.etat = "" 
        for particule in self.__particules:
            particule.update(self.__dt)
            particule.draw(self.ecran)
        self.__particules = [e for e in self.__particules if not e.est_terminee()]
        if self.__particules == []:
            self.__jeu.etat = "Victoire"
            self.__listePosGagnante = None

    def UtilisationSort(self, resultatPosition: tuple)-> None:
        for ind, sort in enumerate(self.__jeu.sorts[self.__jeu.joueur]):
            if sort == "Clique":
                if ind == 0:
                    sortUtilise = self.__jeu.SortBloqueColonne(resultatPosition[1][1])
                    if sortUtilise:
                        self.__jeu.sortConso = True
                elif ind == 1:
                    if self.__jeu.grille.grille[0][resultatPosition[1][1]] != "r" and self.__jeu.grille.grille[0][resultatPosition[1][1]] != "j" and self.__jeu.grille.grille[0][resultatPosition[1][1]] != "n":
                        self.__jeu.sortConso = True
                        self.__jeu.jetonNoir = True
                        self.ActivationVariableDePlacement(resultatPosition[1][1])
                else:
                    sortUtilise, self.__listePosGagnante = self.__jeu.SortFantome(resultatPosition[1])
                    if sortUtilise:
                        self.__boutonFantomeActif = False
                        self.__jeu.sortUtilise = True
                        self.CreerParticules()

    def CalculerCoupIa(self, numero: int)-> None:
        """Calcule le coup de l'IA sur une copie de la grille (tourne dans un thread)"""
        colonne = IA.best_placement(self.__jeu.grille)
        if numero == self.__numeroPartie:   # la partie n'a pas été réinitialisée entre-temps
            self.__resultatIa = colonne

#Lancement de la class qui créé le jeu
if __name__ == "__main__":
    Main().Update()