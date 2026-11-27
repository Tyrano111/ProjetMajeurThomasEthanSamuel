import pygame
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
        self.clock = pygame.time.Clock()
        self.jeu = Jeu()

        #Ui :
        self.accueil = UI.Accueil()
        self.uiPause = UI.Pause()
        self.uiGrille = UI.Grille()
        self.jeton = UI.Jeton()
        self.boutons = {
            "r" : [UI.BoutonSort((1050, 175), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 375), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 575), 128, "Assets/BoutonFantome")], 
            "j" : [UI.BoutonSort((1050, 175), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 375), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 575), 128, "Assets/BoutonFantome")]
            }
        self.victoire = UI.Victoire()

        #Variables pour le placement des jetons et le bon deroulement du tour
        self.__estEnChute = False
        self.__indiceFuturPosition = (0, 0)
        self.__positionFuturJeton = (0, 0)
        self.__forceRebon = 0

        #Variables Ia
        self.__tourIa = False

        #Variable pour les sorts
        self.__indSortEnCour = 0
        self.__boutonFantomeActif = False

        #Varible pour les particules
        self.listePosGagnante = None
        self.particules = []
        self.dt = None
        self.puissanceMax = False
        

    def Update(self):
        """fonction qui gére tout le jeu. Elle change les ecrans au bon moment et s'occupe de la base de pygame"""
        while self.jeu.etat != "":
            self.ecran.fill("black")
            self.dt = self.clock.tick(60) / 500
            if self.jeu.etat == "Accueil":
                self.UpdateAccueil()
            elif self.jeu.etat == "Victoire" or self.jeu.etat == "Egalite":
                self.UpdateVictoire()
            else:
                if self.jeu.echap:
                    self.UpdatePause()
                elif self.jeu.etat == "Solo":
                    self.UpdateSolo()
                else:
                    self.UpdateJcj()
                
            pygame.display.flip()
        pygame.quit()


    def UpdateAccueil(self):
        """fonction qui s'occupe de l'accueil, elle l'affiche et permet de faire les action à l'interieur"""
        self.accueil.draw(self.ecran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.accueil.BoutonClique(mouse)
                if clique != 0:
                    if clique == 1:
                        self.jeu.etat = "Solo"
                    elif clique == 2:
                        self.jeu.etat = "Jcj"
                    else:
                        self.jeu.etat = ""


    def UpdateSolo(self):
        """fonction qui s'occupe du mode solo, elle l'affiche et permet de faire les action à l'interieur"""
        self.PlacementJeton()
        self.Interfacejeu()
        if self.listePosGagnante is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jeu.etat = "" 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.jeu.echap = True
                elif not self.__estEnChute and not self.__tourIa:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()
                            resultatPosition = self.EmplacementSourieGrille(mouse)
                            if resultatPosition[0]:
                                self.ActivationVariableDePlacement(resultatPosition[1][1])
            if self.__tourIa and not self.__estEnChute:
                colonePlace = IA.best_placement(self.jeu.grille)
                self.ActivationVariableDePlacement(colonePlace)
        else:
            for particule in self.particules:
                particule.update(self.dt)
                particule.draw(self.ecran)
            
            self.particules = [e for e in self.particules if not e.est_terminee()]
            if self.particules == []:
                self.jeu.etat = "Victoire"
                self.listePosGagnante = None
        
        

    def UpdateJcj(self):
        """fonction qui s'occupe du mode joueur contre joueur, elle l'affiche et permet de faire les action à l'interieur"""
        self.PlacementJeton()
        self.Interfacejeu()
        if self.listePosGagnante is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.jeu.etat = "" 
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.jeu.echap = True
                elif not self.__estEnChute:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse = pygame.mouse.get_pos()
                            resultatPosition = self.EmplacementSourieGrille(mouse)
                            if resultatPosition[0]:
                                if not self.jeu.sortConso:
                                    for ind, sort in enumerate(self.jeu.sorts[self.jeu.joueur]):
                                        if sort == "Clique":
                                            if ind == 0:
                                                sortUtilise = self.jeu.SortBloqueColonne(resultatPosition[1][1])
                                                if sortUtilise:
                                                    self.jeu.sortConso = True
                                            elif ind == 1:
                                                if self.jeu.grille.grille[0][resultatPosition[1][1]] != "r" and self.jeu.grille.grille[0][resultatPosition[1][1]] != "j" and self.jeu.grille.grille[0][resultatPosition[1][1]] != "n":
                                                    self.jeu.sortConso = True
                                                    self.jeu.jetonNoir = True
                                                    self.ActivationVariableDePlacement(resultatPosition[1][1])
                                            else:
                                                sortUtilise, self.listePosGagnante = self.jeu.SortFantome(resultatPosition[1])
                                                if sortUtilise:
                                                    self.__boutonFantomeActif = False
                                                    self.jeu.sortUtilise = True
                                                    self.CreerParticules()  
                                if not self.jeu.sortUtilise:
                                    self.ActivationVariableDePlacement(resultatPosition[1][1])
                            elif not self.jeu.sortConso:
                                etatSortJoueur = self.jeu.sorts[self.jeu.joueur]
                                for ind, bouton in enumerate(self.boutons[self.jeu.joueur]):
                                    if etatSortJoueur[ind] != "Utilise":
                                        if bouton.est_clique(mouse) and etatSortJoueur[ind] == "Normal":
                                            if self.__indSortEnCour != ind and etatSortJoueur[self.__indSortEnCour] == "Clique":
                                                self.jeu.SelectionnerEtatSort("Normal", self.__indSortEnCour)
                                                
                                                self.__indSortEnCour = ind
                                            self.jeu.SelectionnerEtatSort("Clique", ind)
                                            self.__indSortEnCour = ind
                                            
                                            if ind == 2:
                                                self.__boutonFantomeActif = True
                                            else:
                                                self.__boutonFantomeActif = False
                                        elif bouton.est_clique(mouse) and etatSortJoueur[ind] == "Clique":
                                            self.jeu.SelectionnerEtatSort("Normal", ind)
                                            
                                            self.__boutonFantomeActif = False
        else:
            for particule in self.particules:
                particule.update(self.dt)
                particule.draw(self.ecran)
            self.particules = [e for e in self.particules if not e.est_terminee()]
            if self.particules == []:
                self.jeu.etat = "Victoire"
                self.listePosGagnante = None
                                
        

    def UpdatePause(self):
        """fonction qui s'occupe du menu de pause, elle l'affiche et permet de faire les action à l'interieur"""
        self.Interfacejeu()
        self.uiPause.draw(self.ecran)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.uiPause.BoutonClique(mouse)
                if clique == 1:
                    self.jeu.echap = False
                if clique == 2:
                    self.ReinitialiserJeu()

    def UpdateVictoire(self):
        """fonction qui s'occupe du menu de victoire, elle l'affiche et permet de faire les action à l'interieur"""
        self.victoire.draw(self.ecran, self.jeu.joueur, self.jeu.etat)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.victoire.boutonMenu.est_clique(mouse):
                    self.ReinitialiserJeu()

    def ReinitialiserJeu(self):
        """fonction qui reinitilise toutes les variables du jeu pour pouvoir en relancer une sans être affecté par les autres"""
        self.jeu.ReinitialiserPartie()
        self.jeton.ReinitialiserJeton()
        self.__tourIa = False
        self.__estEnChute = False
        self.__boutonFantomeActif = False
        self.__indSortEnCour = 0
        self.particules = []
        self.puissanceMax = False
        self.listePosGagnante = None

    def Interfacejeu(self):
        """fonction qui affiche tout l'ecran de jeu, elle affiche la grille et les boutons de sort"""
        mouse = pygame.mouse.get_pos()
        self.uiGrille.draw(self.jeu.grille.grille, self.ecran, mouse, self.__boutonFantomeActif, self.jeu.joueur)
        if self.jeu.etat != "Solo":
            for i in range(len(self.boutons[self.jeu.joueur])):
                self.boutons[self.jeu.joueur][i].draw(self.ecran, self.jeu.sorts[self.jeu.joueur][i])

    def EmplacementSourieGrille(self, mouse):
        """fonction permettant de savoir ou se situe la sourie sur la grille. Elle renvoie un tuple avec est ce que la sourie est dans la grille et sa position"""
        for indLigne, ligne in enumerate(self.jeu.grille.grille):
            posLigne = CV.POS_GRILLE_Y + indLigne * CV.TAILLE_CASE
            for indColonne in range(len(ligne)):
                posColone = CV.POS_GRILLE_X + indColonne * CV.TAILLE_CASE
                rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    return True, (indLigne, indColonne)
        return False, None

    def TransformationIndiceEnPositon(self, indice):
        """fonction qui transforme un indice de grille en position"""
        return CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE, CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE

    def TransformationIndiceEnPositonParticule(self, indice):
        """fonction qui transforme un indice de grille en position pour le placer au millieu d'un jeton"""
        return (
            CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE + CV.TAILLE_CASE // 2,
            CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE + CV.TAILLE_CASE // 2
        )

    def PlacementJeton(self):
        """fonction pour faire les actions du jeu.
        elle permet de poser un jeton ou de jouer un sort"""
        if self.__estEnChute:
            self.__forceRebon = self.jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, "n") if self.jeu.jetonNoir else self.jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, self.jeu.joueur)
            if self.__forceRebon == 0:
                if self.jeu.etat == "Solo":
                    self.__tourIa = False if self.__tourIa else True

                if self.jeu.jetonNoir:
                    self.listePosGagnante = self.jeu.SortJetonNoir(self.__indiceFuturPosition[1])

                else:
                    self.listePosGagnante = self.jeu.JouerCoup(self.__indiceFuturPosition[1])
                
                self.CreerParticules()
                self.__estEnChute = False
                self.jeton.position[1] = 0
        if self.jeu.sortUtilise:
            self.jeu.sortUtilise = False

    def ActivationVariableDePlacement(self, indcolonne):
        """fonction permettant de lancer le placement du jeton"""
        self.__indiceFuturPosition = indcolonne
        self.__indiceFuturPosition = self.jeu.grille.trouve_position(indcolonne)
        if self.__indiceFuturPosition is not None:
            self.__estEnChute = True
            self.__positionFuturJeton = self.TransformationIndiceEnPositon(self.__indiceFuturPosition)
            self.__forceRebon = CV.DICT_FORCE_REBON[self.__indiceFuturPosition[0]]


    def CreerParticules(self):
        """fonction creant les particules en cas de victoire"""
        if self.listePosGagnante is not None:
            if len(self.listePosGagnante) >= 5:
                self.puissanceMax = True
            self.particules = []
            for ind in self.listePosGagnante:
                position = self.TransformationIndiceEnPositonParticule(ind)
                particule = UI.Particule(position, 200, self.jeu.joueur, self.puissanceMax)
                self.particules.append(particule)


#Lancement de la class qui créé le jeu
Main().Update()