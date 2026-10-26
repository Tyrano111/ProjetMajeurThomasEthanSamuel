#Script central c'est lui qui lance le jeu et permet de tout connecter
import UI
import Game
import ConstantesEtVariable as CV
import pygame


victoire = False

class Main:
    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode(CV.TAILLE_FENETRE)
        pygame.display.set_caption("Puissance 4.5")
        self.clock = pygame.time.Clock()
        self.etat = "Menu"
        self.echap = False
        self.joueur = "r"
        self.grille = UI.Grille()
        self.bouton1 = UI.BoutonRond((950, 150), 45, "Assets/JetonRouge.png")
        self.bouton2 = UI.BoutonRond((950, 350), 45, "Assets/JetonJaune.png")
        self.bouton3 = UI.BoutonRond((950, 550), 45, "Assets/JetonRouge.png")
        self.accueil = UI.Menu("Accueil")
        self.pause = UI.Menu("Pause")
        self.jeton_jaune = UI.Jeton("j")
        self.jeton_rouge = UI.Jeton("r")
        self.est_en_chute = False
        self.indice_futur_jeton = ()
        self.position_futur_jeton = ()
        self.force_rebon = 0

    def UpdateJeu(self):
        while self.etat == "Jeu":
            self.ecran.fill("black")

            if self.echap:
                self.UpdatePause()
            else:

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.etat = ""
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.echap = True
                    elif not self.est_en_chute:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                resultat = self.place_jeton(pygame.mouse.get_pos())
                                if resultat != None:
                                    self.est_en_chute, self.indice_futur_jeton, self.force_rebon = resultat
                                    self.position_futur_jeton = self.indice_a_position(self.indice_futur_jeton)

                self.PlacementJeton()

                self.InterfaceDeJeu()
            
            pygame.display.flip()
            
            self.clock.tick(60)


    def UpdateAccueil(self):
        while self.etat == "Menu":
            self.ecran.fill("black")
            
            self.accueil.draw(self.ecran)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.etat = ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    clique = self.accueil.BoutonClique(mouse)
                    if clique == 1:
                        self.etat = "Jeu"
                        self.UpdateJeu()
                    if clique == 2:
                        self.etat = ""
                        
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


    def UpdatePause(self):
        self.grille.draw(self.ecran)
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
                    CV.grille = [["", "", "", "", "", "", ""] for i in range(6)]

    def indice_a_position(self, indice):
        return CV.POS_GRILLE_X + indice[1] * CV.TAILLE_CASE, CV.POS_GRILLE_Y + indice[0] * CV.TAILLE_CASE

    def PlacementJeton(self):
        if self.est_en_chute:
            self.force_rebon = self.jeton_jaune.rebon(self.ecran, self.position_futur_jeton, self.force_rebon) if self.joueur == "j" else self.jeton_rouge.rebon(self.ecran, self.position_futur_jeton, self.force_rebon)
            if self.force_rebon == 0:
                self.est_en_chute = False
                CV.grille[self.indice_futur_jeton[0]][self.indice_futur_jeton[1]] = self.joueur
                self.jeton_jaune.position[1] = 0
                self.jeton_rouge.position[1] = 0
                gagnant = Game.winner(CV.grille, self.indice_futur_jeton, "j") if self.joueur == "j" else Game.winner(CV.grille, self.indice_futur_jeton, "r")
                if gagnant:
                    print("r" if self.joueur == "r" else "j")
                self.joueur = "j" if self.joueur == "r" else "r"

    def InterfaceDeJeu(self):
        self.grille.draw(self.ecran)
        self.bouton1.draw(self.ecran)
        self.bouton2.draw(self.ecran)
        self.bouton3.draw(self.ecran)

    def place_jeton(self, mouse):
        for indLigne, ligne in enumerate(CV.grille):
            posLigne = CV.POS_GRILLE_Y + indLigne * CV.TAILLE_CASE
            for indColone in range(len(ligne)):
                posColone = CV.POS_GRILLE_X + indColone * CV.TAILLE_CASE
                rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    indice_arret = Game.trouve_position(CV.grille, indColone)
                    if indice_arret[0]:
                        return True, (indice_arret[1], indColone), CV.DICT_FORCE_REBON[indice_arret[1]]

Main().UpdateAccueil()