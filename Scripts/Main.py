#Script central c'est lui qui lance le jeu et permet de tout connecter
import UI
import IA
import Game
import ConstantesEtVariable as CV
import pygame

class Main:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode(CV.TAILLE_FENETRE)
        pygame.display.set_caption("Puissance 4.5")
        self.clock = pygame.time.Clock()
        self.etat = "Menu"
        self.echap = False
        self.joueur = "r"
        self.uiGrille = UI.Grille()
        self.victoire = UI.Victoire()
        self.etatSorts = {"r" : ["Normal", "Normal", "Normal"], "j": ["Normal", "Normal", "Normal"]}
        self.boutons = {"r" : [UI.BoutonSort((1050, 100), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 300), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 500), 128, "Assets/BoutonFantome")], "j" : [UI.BoutonSort((1050, 100), 128, "Assets/BoutonSort1"), UI.BoutonSort((1050, 300), 128, "Assets/BoutonJetonNoir"), UI.BoutonSort((1050, 500), 128, "Assets/BoutonFantome")]}
        self.indSortEnCour = 0
        self.accueil = UI.Menu("Accueil")
        self.pause = UI.Menu("Pause")
        self.jeton = UI.Jeton()
        self.est_en_chute = False
        self.indice_futur_jeton = (0, 0)
        self.position_futur_jeton = ()
        self.force_rebon = 0
        self.compteurSort = 2
        self.jetonNoir = False
        self.sortFantomeClique = False
        self.tourIa = False

    def Update(self):
        while self.etat != "":
            self.ecran.fill("black")

            if self.etat == "Menu": 
                self.UpdateAccueil()
            elif self.etat == "Jeu":
                if self.echap:
                    self.UpdatePause()
                else:
                    self.UpdateJeu()
            elif self.etat == "Solo":
                if self.echap:
                    self.UpdatePause()
                else:
                    self.UpdateSolo()
            else: 
                self.UpdateVictoire()

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
            
    def UpdateSolo(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.echap = True
            elif not self.est_en_chute and not self.tourIa:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse = pygame.mouse.get_pos()
                        resultat = self.place_jeton(mouse) 
                        if resultat != None:
                            self.est_en_chute, self.indice_futur_jeton, self.force_rebon = resultat
                            self.position_futur_jeton = self.indice_a_position(self.indice_futur_jeton)
        if self.tourIa and not self.est_en_chute:
            colonePlace = IA.best_placement(Game.grille, self.joueur)
            self.indice_futur_jeton = Game.trouve_position(colonePlace, self.joueur)[1], colonePlace
            self.position_futur_jeton = self.indice_a_position(self.indice_futur_jeton)
            self.force_rebon = CV.DICT_FORCE_REBON[self.indice_futur_jeton[0]]
            self.est_en_chute = True
        self.PlacementJeton()
        self.InterfaceDeJeu()


        



    def UpdateJeu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.echap = True
            elif not self.est_en_chute:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        resultat = None
                        mouse = pygame.mouse.get_pos()
                        for ind, etat in enumerate(self.etatSorts[self.joueur]):
                            if etat == "Clique":
                                if ind == 0:
                                    self.BloqueColonne(mouse)
                                    resultat = ""
                                elif ind == 1:
                                    self.jetonNoir = True
                                else:
                                    self.PlaceFantome(mouse)
                                    resultat = ""
                        resultat = self.place_jeton(mouse) if resultat == None else None
                        if resultat != None:
                            self.est_en_chute, self.indice_futur_jeton, self.force_rebon = resultat
                            self.position_futur_jeton = self.indice_a_position(self.indice_futur_jeton)
                        for i in range(len(self.boutons[self.joueur])):
                            if self.etatSorts[self.joueur][i] != "Utilisé":
                                if self.boutons[self.joueur][i].est_clique(mouse) and self.etatSorts[self.joueur][i] == "Normal":
                                    if i != self.indSortEnCour and self.etatSorts[self.joueur][self.indSortEnCour] == "Clique":
                                        self.etatSorts[self.joueur][self.indSortEnCour] = "Normal"
                                        self.boutons[self.joueur][self.indSortEnCour].position = (self.boutons[self.joueur][self.indSortEnCour].position[0] + 5, self.boutons[self.joueur][self.indSortEnCour].position[1] + 5)
                                    self.indSortEnCour = i
                                    self.etatSorts[self.joueur][i] = "Clique"
                                    self.boutons[self.joueur][i].position = (self.boutons[self.joueur][i].position[0] - 5, self.boutons[self.joueur][i].position[1] - 5)
                                    if i == 2:
                                        self.sortFantomeClique = True
                                elif self.boutons[self.joueur][i].est_clique(mouse):
                                    self.etatSorts[self.joueur][i] = "Normal"
                                    self.jetonNoir = False
                                    self.sortFantomeClique = False
                                    self.boutons[self.joueur][i].position = (self.boutons[self.joueur][i].position[0] + 5, self.boutons[self.joueur][i].position[1] + 5)

        self.PlacementJeton()
        self.InterfaceDeJeu()
        


    def UpdateAccueil(self):
        self.accueil.draw(self.ecran)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.accueil.BoutonClique(mouse)
                if clique == 1:
                    self.etat = "Jeu"
                if clique == 2:
                    self.etat = ""

                    

    def UpdatePause(self):
        self.uiGrille.draw(Game.grille, self.ecran, (0, 0), False)
        self.pause.draw(self.ecran)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                clique = self.pause.BoutonClique(mouse)
                if clique == 1:
                    self.echap = False
                if clique == 2:
                    self.echap = False
                    self.etat = "Menu"
                    self.ReinitialiserJeu()

    def UpdateVictoire(self):
        self.victoire.draw(self.ecran, self.joueur)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.victoire.boutonMenu.est_clique(mouse):
                    self.echap = False
                    self.etat = "Menu"
                    self.ReinitialiserJeu()

    def indice_a_position(self, indice):
        return CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE, CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE

    def PlacementJeton(self):
        if self.est_en_chute:
            self.force_rebon = self.jeton.rebon(self.ecran, self.position_futur_jeton, self.force_rebon, "n") if self.jetonNoir else self.jeton.rebon(self.ecran, self.position_futur_jeton, self.force_rebon, self.joueur)
            if self.force_rebon == 0:
                self.est_en_chute = False
                Game.grille[self.indice_futur_jeton[0]][self.indice_futur_jeton[1]] = "n" if self.jetonNoir else self.joueur
                if self.jetonNoir:
                    self.jetonNoir = False
                    self.UtilisationDuBouton()
                else:
                    self.compteurSort -= 1
                    gagnant = Game.winner(self.indice_futur_jeton, self.joueur) 
                    if gagnant:
                        self.etat = "Victoire"
                    else:
                        self.joueur = "j" if self.joueur == "r" else "r"
                        if self.etat == "Solo":
                            self.tourIa = False if self.tourIa else True
                if self.etat == "Solo":
                    posFantome, couleurFantome = Game.desbloque_fantome(self.indice_futur_jeton)
                    while posFantome != None:
                        gagnant = Game.winner(posFantome, couleurFantome)
                        if gagnant:
                            self.etat = "Victoire"
                        posFantome, couleurFantome = Game.desbloque_fantome(posFantome)
                self.jeton.position[1] = 0
        if self.compteurSort == 0:
            Game.desbloque_colonne(self.joueur)

    def InterfaceDeJeu(self):
        mouse = pygame.mouse.get_pos()
        self.uiGrille.draw(Game.grille, self.ecran, mouse, self.sortFantomeClique, self.joueur)
        for i in range(len(self.boutons[self.joueur])):
            self.boutons[self.joueur][i].draw(self.ecran, self.etatSorts[self.joueur][i])

    def ReinitialiserJeu(self):
        Game.grille = [[" ", " ", " ", " ", " ", " ", " "] for i in range(6)]
        self.est_en_chute = False
        self.joueur = "r"

    def place_jeton(self, mouse):
        for indColone in range(7):
            posColone = CV.POS_GRILLE_X + indColone * CV.TAILLE_CASE
            rect = pygame.Rect(posColone, CV.POS_GRILLE_Y, CV.TAILLE_CASE, CV.TAILLE_CASE * 6)
            if rect.collidepoint(mouse):
                indice_arret = Game.trouve_position(indColone, self.joueur)
                if indice_arret[0]:
                    return True, (indice_arret[1], indColone), CV.DICT_FORCE_REBON[indice_arret[1]]

    def BloqueColonne(self, mouse):
        for indColone in range(7):
            posColone = CV.POS_GRILLE_X + indColone * CV.TAILLE_CASE
            rect = pygame.Rect(posColone, CV.POS_GRILLE_Y, CV.TAILLE_CASE, CV.TAILLE_CASE * 6)
            if rect.collidepoint(mouse):
                Game.bloque_colonne(indColone, self.joueur)
                self.compteurSort = 2
                self.UtilisationDuBouton()
                

    def PlaceFantome(self, mouse):
        for indLigne, ligne in enumerate(Game.grille):
            posLigne = CV.POS_GRILLE_Y + indLigne * CV.TAILLE_CASE
            for indColone in range(len(ligne)):
                posColone = CV.POS_GRILLE_X + indColone * CV.TAILLE_CASE
                rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    Game.fantome((indLigne, indColone), self.joueur)
                    self.UtilisationDuBouton()
                    posFantome, couleurFantome = Game.desbloque_fantome(self.indice_futur_jeton)
                    while posFantome != None:
                        gagnant = Game.winner(posFantome, couleurFantome)
                        if gagnant:
                            self.etat = "Victoire"
                        posFantome, couleurFantome = Game.desbloque_fantome(posFantome)
                    self.joueur = "j" if self.joueur == "r" else "r"

    def UtilisationDuBouton(self):
        for i in range(len(self.boutons[self.joueur])):
            if self.etatSorts[self.joueur][i] == "Clique":
                self.etatSorts[self.joueur][i] = "Utilisé"
                self.boutons[self.joueur][i].position = (self.boutons[self.joueur][i].position[0] + 5, self.boutons[self.joueur][i].position[1] + 5)
                for ind, etatSort in enumerate(self.etatSorts[self.joueur]):
                    if etatSort != self.etatSorts[self.joueur][i]:
                        self.indSortEnCour = ind


Main().Update()