import pygame
from Jeu import Jeu
import ConstantesEtVariable as CV
import UI
import IA


class MainBys:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode(CV.TAILLE_FENETRE)
        pygame.display.set_caption("Puissance 4.5")
        self.clock = pygame.time.Clock()

        self.jeu = Jeu()

        #Ui :
        self.accueil = UI.Menu("Accueil")
        self.uiGrille = UI.Grille()
        self.jeton = UI.Jeton()
        self.pause = UI.Menu("Pause")
        self.boutons = {
            "r" : [UI.BoutonSort((1050, 100), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 300), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 500), 128, "Assets/BoutonFantome")], 
            "j" : [UI.BoutonSort((1050, 100), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 300), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 500), 128, "Assets/BoutonFantome")]
            }
        self.victoire = UI.Victoire()

        self.__estEnChute = False
        self.__indiceFuturPosition = (0, 0)
        self.__positionFuturJeton = (0, 0)
        self.__forceRebon = 0
        self.__tourIa = False
        self.__indSortEnCour = 0
        self.__boutonFantomeActif = False
        

    def Update(self):
        while self.jeu.etat != "":
            self.ecran.fill("black")

            if self.jeu.etat == "Accueil":
                self.UpdateAccueil()
            elif self.jeu.etat == "Victoire":
                self.UpdateVictoire()
            else:
                if self.jeu.echap:
                    self.UpdatePause()
                elif self.jeu.etat == "Solo":
                    self.UpdateSolo()
                else:
                    self.UpdateJcj()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


    def UpdateAccueil(self):
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
        
        
        self.PlacementJeton()
        self.Interfacejeu()


    def UpdateJcj(self):

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
                                        self.jeu.sortUtilise = True
                                        self.jeu.sortConso = True
                                        if ind == 0:
                                            self.jeu.SortBloqueColonne(resultatPosition[1][1])
                                            self.ChangementPositionBoutonSort(ind, "Clique")
                                        elif ind == 1:
                                            self.jeu.jetonNoir = True
                                            self.ActivationVariableDePlacement(resultatPosition[1][1])
                                        else:
                                            self.ChangementPositionBoutonSort(ind, "Clique")
                                            self.jeu.SortFantome(resultatPosition[1])
                                            self.__boutonFantomeActif = False
                            if not self.jeu.sortUtilise:
                                self.ActivationVariableDePlacement(resultatPosition[1][1])
                        elif not self.jeu.sortConso:
                            etatSortJoueur = self.jeu.sorts[self.jeu.joueur]
                            for ind, bouton in enumerate(self.boutons[self.jeu.joueur]):
                                if etatSortJoueur[ind] != "Utilise":
                                    if bouton.est_clique(mouse) and etatSortJoueur[ind] == "Normal":
                                        if self.__indSortEnCour != ind and etatSortJoueur[self.__indSortEnCour] == "Clique":
                                            self.jeu.SelectionnerEtatSort("Normal", self.__indSortEnCour)
                                            self.ChangementPositionBoutonSort(self.__indSortEnCour, "Clique")
                                            self.__indSortEnCour = ind
                                        self.jeu.SelectionnerEtatSort("Clique", ind)
                                        self.__indSortEnCour = ind
                                        self.ChangementPositionBoutonSort(ind, "Normal")
                                        if ind == 2:
                                            self.__boutonFantomeActif = True
                                    elif bouton.est_clique(mouse) and etatSortJoueur[ind] == "Clique":
                                        self.jeu.SelectionnerEtatSort("Normal", ind)
                                        self.ChangementPositionBoutonSort(ind, "Clique")
                                        self.__boutonFantomeActif = False
                                
        self.PlacementJeton()
        self.Interfacejeu()

    def UpdatePause(self):
        self.Interfacejeu()
        self.pause.draw(self.ecran)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.pause.BoutonClique(mouse)
                if clique == 1:
                    self.jeu.echap = False
                if clique == 2:
                    self.ReinitialiserJeu()

    def UpdateVictoire(self):
        self.victoire.draw(self.ecran, self.jeu.joueur)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.jeu.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.victoire.boutonMenu.est_clique(mouse):
                    self.ReinitialiserJeu()

    def ReinitialiserJeu(self):
        self.jeu.ReinitialiserPartie()

    def Interfacejeu(self):
        mouse = pygame.mouse.get_pos()
        self.uiGrille.draw(self.jeu.grille.grille, self.ecran, mouse, self.__boutonFantomeActif, self.jeu.joueur)
        if self.jeu.etat != "Solo":
            for i in range(len(self.boutons[self.jeu.joueur])):
                self.boutons[self.jeu.joueur][i].draw(self.ecran, self.jeu.sorts[self.jeu.joueur][i])

    def EmplacementSourieGrille(self, mouse):
        for indLigne, ligne in enumerate(self.jeu.grille.grille):
            posLigne = CV.POS_GRILLE_Y + indLigne * CV.TAILLE_CASE
            for indColonne in range(len(ligne)):
                posColone = CV.POS_GRILLE_X + indColonne * CV.TAILLE_CASE
                rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    return True, (indLigne, indColonne)
        return False, None

    def TransformationIndiceEnPositon(self, indice):
        return CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE, CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE

    def PlacementJeton(self):
        if self.__estEnChute:
            self.__forceRebon = self.jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, "n") if self.jeu.jetonNoir else self.jeton.rebon(self.ecran, self.__positionFuturJeton, self.__forceRebon, self.jeu.joueur)
            if self.__forceRebon == 0:
                if self.jeu.etat == "Solo":
                    self.__tourIa = False if self.__tourIa else True

                if self.jeu.jetonNoir:
                    self.jeu.SortJetonNoir(self.__indiceFuturPosition[1])
                    self.ChangementPositionBoutonSort(1, "Clique")

                else:
                    self.jeu.JouerCoup(self.__indiceFuturPosition[1])

                self.__estEnChute = False
                self.jeton.position[1] = 0
        if self.jeu.sortUtilise:
            self.jeu.sortUtilise = False

    def ActivationVariableDePlacement(self, indcolonne):
        self.__indiceFuturPosition = indcolonne
        self.__indiceFuturPosition = self.jeu.grille.trouve_position(indcolonne)
        if self.__indiceFuturPosition is not None:
            self.__estEnChute = True
            self.__positionFuturJeton = self.TransformationIndiceEnPositon(self.__indiceFuturPosition)
            self.__forceRebon = CV.DICT_FORCE_REBON[self.__indiceFuturPosition[0]]

    def ChangementPositionBoutonSort(self, ind, etat):
        positionBouton = self.boutons[self.jeu.joueur][ind].position
        if etat == "Normal":
            self.boutons[self.jeu.joueur][ind].position = (positionBouton[0] - 5, positionBouton[1] - 5)
        else:
            self.boutons[self.jeu.joueur][ind].position = (positionBouton[0] + 5, positionBouton[1] + 5)

MainBys().Update()