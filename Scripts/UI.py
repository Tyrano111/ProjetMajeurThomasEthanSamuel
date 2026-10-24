#Il s'occupe de toute la partie graphique avec pygame
import pygame
import Constantes

class Ui:
    """ La class UI permet de gerer toute la partie graphique du projet. Elle s'occupe de ça grâce au module pygame """
    def __init__(self):
        """ Fonction d'intialisation de le class. Elle lance Pygame et gere les variables de base """
        #Variable de la Classe
        self.joueur = "Joueur Rouge"

        #Lancement de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(Constantes.TAILLE_FENETRE)
        pygame.display.set_caption("Puissance 4.5")
        self.font = pygame.font.SysFont("Corbel", 40)
        self.clock = pygame.time.Clock()
        self.etat = "Menu"
        self.echap = False
        
        #Varible dependant de Pygame
        self.boutonJouer = pygame.Rect((800-140)/2, (600 - 50)/2 - 35, 300, 150)
        self.assetBoutonJouer = pygame.image.load("Assets/BoutonJouer.png")
        self.boutonQuitter = pygame.Rect((800-140)/2, (600-50)/2 + 35, 140, 50)
        self.continuer = pygame.Rect((800-140)/2, (600 - 50)/2 - 35, 220, 50)
        self.retourMenu = pygame.Rect((800-140)/2, (600-50)/2 + 35, 220, 50)
        self.assetGrille = pygame.image.load("Assets/Grille.png")
        self.colone = pygame.image.load("Assets/ColoneGrille.png")
        self.coloneSurvole = pygame.image.load("Assets/ColoneGrilleSurvole.png")
        self.jetonJaune = pygame.image.load("Assets/JetonJaune.png")
        self.jetonRouge = pygame.image.load("Assets/JetonRouge.png")
        self.positionJetonX = 0
        self.positionJetonY = 0
        self.gravite = 2
        self.forceRebon = 0
        self.positionLigneArret = 0
        self.estEnChute = False
        self.positionJetonGrille = ()


    def Main(self):
        
        while self.etat == "Jeu":
            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")
        
            if self.echap:
                self.AfficherGrille()
                self.MenuDePause()
            else:
                # poll for events
                # pygame.QUIT event means the user clicked X to close your window
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.etat = ""
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            Constantes.GRILLE = [ [0, 0, 0, 0, 0, 0, 0] for i in range(6)]
                            self.joueur = "Joueur Rouge"
                        elif event.key == pygame.K_ESCAPE:
                            self.echap = True
                    elif not self.estEnChute:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                self.MouseCollision(pygame.mouse.get_pos())
                if self.estEnChute:
                    self.RebonJeton()
                self.AfficherGrille()
                
            
            # RENDER YOUR GAME HERE
            
            
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
        
    def AfficherGrille(self):
        mouse = pygame.mouse.get_pos()
    
        for position in Constantes.POS_COLONES_GRILLE:
            rect = pygame.Rect(position-7, Constantes.POS_GRILLE_Y-7, Constantes.TAILLE_CASE + Constantes.ESPACE_CASE, Constantes.TAILLE_CASE*7 + Constantes.ESPACE_CASE*7)
            if rect.collidepoint(mouse): 
                self.screen.blit(self.coloneSurvole, (position-7, Constantes.POS_GRILLE_Y-7))
            else:
                self.screen.blit(self.colone, (position-7, Constantes.POS_GRILLE_Y-7))
        for indL, ligne in enumerate(Constantes.GRILLE):
            for indC, case in enumerate(ligne):
                posX = Constantes.POS_GRILLE_X + indC * Constantes.TAILLE_CASE + indC * Constantes.ESPACE_CASE + 4
                posY = Constantes.POS_GRILLE_Y + indL * Constantes.TAILLE_CASE + indL * Constantes.ESPACE_CASE + 4
                if case == 1:
                    self.screen.blit(self.jetonJaune, (posX, posY))
                elif case == 2:
                    self.screen.blit(self.jetonRouge, (posX, posY))

    def MouseCollision(self, mouse):
        for indL, ligne in enumerate(Constantes.GRILLE):
            for indC, case in enumerate(ligne):
                posX = Constantes.POS_GRILLE_X + indC * Constantes.TAILLE_CASE + indC * Constantes.ESPACE_CASE
                posY = Constantes.POS_GRILLE_Y + indL * Constantes.TAILLE_CASE + indL * Constantes.ESPACE_CASE
                rect = pygame.Rect(posX, posY, Constantes.TAILLE_CASE, Constantes.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    if case == 0:
                        self.positionJetonGrille = (indL, indC)
                        self.forceRebon = Constantes.DICT_FORCE_REBON[indL]
                        self.positionLigneArret = Constantes.POS_GRILLE_Y + (Constantes.TAILLE_CASE + Constantes.ESPACE_CASE) * indL + 4
                        self.positionJetonX = Constantes.POS_GRILLE_X + (Constantes.TAILLE_CASE + Constantes.ESPACE_CASE) * indC + 4
                        self.positionJetonY = 0
                        self.estEnChute = True

    def MenuDePause(self):
        self.screen.blit(self.assetGrille, (Constantes.POS_GRILLE_X-7, Constantes.POS_GRILLE_Y-7))
    
        for indL, ligne in enumerate(Constantes.GRILLE):
            for indC, case in enumerate(ligne):
                posX = Constantes.POS_GRILLE_X + indC * Constantes.TAILLE_CASE + indC * Constantes.ESPACE_CASE + 4
                posY = Constantes.POS_GRILLE_Y + indL * Constantes.TAILLE_CASE + indL * Constantes.ESPACE_CASE + 4
                if case == 1:
                    self.screen.blit(self.jetonJaune, (posX, posY))
                elif case == 2:
                    self.screen.blit(self.jetonRouge, (posX, posY))
    
        pygame.draw.rect(self.screen, (255, 255, 255), self.continuer)
        pygame.draw.rect(self.screen, (255, 255, 255), self.retourMenu)
                    
        play_text = self.font.render("Continuer", True, (0, 0, 0))
        quit_text = self.font.render("Retour Menu", True, (0, 0, 0))
                    
        self.screen.blit(play_text, ((800-140)/2 + 25, (600 - 50)/2 - 35 + 7))
        self.screen.blit(quit_text, ((800-140)/2 + 10, (600 - 50)/2 - 35 + 80))
    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.etat = ""
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if self.continuer.collidepoint(mouse):
                    self.echap = False
                if self.retourMenu.collidepoint(mouse):
                    self.echap = False
                    self.etat = "Menu"
                    Constantes.GRILLE = [[0, 0, 0, 0, 0, 0, 0] for i in range(6)]
    
    def MenuDeDemarage(self):
        while self.etat == "Menu":

            self.screen.fill("black")

            self.screen.blit(self.assetBoutonJouer, self.boutonJouer)
            """
            pygame.draw.rect(self.screen, (255, 255, 255), self.boutonQuitter)

            quit_text = self.font.render("Quitter", True, (0, 0, 0))

            self.screen.blit(quit_text, ((800-140)/2 + 10, (600 - 50)/2 - 35 + 80))"""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.etat = ""
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if self.boutonJouer.collidepoint(mouse):
                        self.etat = "Jeu"
                        self.Main()
                    if self.boutonQuitter.collidepoint(mouse):
                        self.etat = ""
                        
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def RebonJeton(self):
        self.positionJetonY += self.gravite
        self.gravite += 1
        
        if self.joueur == "Joueur Rouge":
            self.screen.blit(self.jetonRouge, (self.positionJetonX, self.positionJetonY))
        else:
            self.screen.blit(self.jetonJaune, (self.positionJetonX, self.positionJetonY))
        if self.positionJetonY >= self.positionLigneArret - self.gravite:
            self.gravite = self.forceRebon
            self.forceRebon /= 2
            if abs(self.forceRebon) <= 0.1:
                if self.joueur == "Joueur Rouge":
                    self.joueur = "Joueur Jaune"
                else:
                    self.joueur = "Joueur Rouge"
                self.estEnChute = False
                Constantes.GRILLE[self.positionJetonGrille[0]][self.positionJetonGrille[1]] = 1 if self.joueur == "Joueur Rouge" else 2

Ui().MenuDeDemarage()