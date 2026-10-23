#Il s'occupe de toute la partie graphique avec pygame
import pygame
import Constantes

class Ui:
    """ La class UI permet de gerer toute la partie graphique du projet. Elle s'occupe de ça grâce au module pygame """
    def __init__(self):
        """ Fonction d'intialisation de le class. Elle lance Pygame et gere les variables de base """
        #Variable de la Classe
        self.joueur = 0

        #Lancement de Pygame
        pygame.init()
        self.screen = pygame.display.set_mode(Constantes.TAILLE_FENETRE, pygame.RESIZABLE)
        pygame.display.set_caption("Puissance 4.5")
        self.font = pygame.font.SysFont("Corbel", 40)
        self.clock = pygame.time.Clock()
        self.etat = "Menu"
        
        #Varible dependant de Pygame
        self.boutonJouer = pygame.Rect((800-140)/2, (600 - 50)/2 - 35, 140, 50)
        self.boutonQuitter = pygame.Rect((800-140)/2, (600-50)/2 + 35, 140, 50)
        self.image = pygame.image.load("Assets/Grille.png")
        self.jetonJaune = pygame.image.load("Assets/JetonJaune.png")
        self.jetonRouge = pygame.image.load("Assets/JetonRouge.png")
        self.posObjX = 0
        self.posObjY = 0
        self.gravity = 2
        self.forceRebon = -7
        self.posL = (0, 0)
        self.chute = False
        self.posG = ()


    def Main(self):
        
        while self.etat == "Jeu":
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.etat = ""
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_f:
                        pygame.display.toggle_fullscreen()
                    elif event.key == pygame.K_g:
                        self.screen = pygame.display.set_mode((800, 600))
                    elif event.key == pygame.K_BACKSPACE:
                        Constantes.GRILLE = [ [0, 0, 0, 0, 0, 0, 0] for i in range(6)]
                elif not self.chute:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.MouseCollision(pygame.mouse.get_pos())

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("black")

            for indL, ligne in enumerate(Constantes.GRILLE):
                for indC, case in enumerate(ligne):
                    posX = Constantes.POS_GRILLE_X + indC * Constantes.TAILLE_CASE + indC * Constantes.ESPACE_CASE + 1
                    posY = Constantes.POS_GRILLE_Y + indL * Constantes.TAILLE_CASE + indL * Constantes.ESPACE_CASE + 1
                    if case == 1:
                        self.screen.blit(self.jetonRouge, (posX, posY))
                    elif case == 2:
                        self.screen.blit(self.jetonJaune, (posX, posY))
            
            
            if self.chute:
                self.RebonJeton()
                

            # RENDER YOUR GAME HERE
            self.screen.blit(self.image, (Constantes.POS_GRILLE_X-7, Constantes.POS_GRILLE_Y-7))
            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60
        

    def MouseCollision(self, mouse):
        for indL, ligne in enumerate(Constantes.GRILLE):
            for indC, case in enumerate(ligne):
                posX = Constantes.POS_GRILLE_X + indC * Constantes.TAILLE_CASE + indC * Constantes.ESPACE_CASE
                posY = Constantes.POS_GRILLE_Y + indL * Constantes.TAILLE_CASE + indL * Constantes.ESPACE_CASE
                rect = pygame.Rect(posX, posY, Constantes.TAILLE_CASE, Constantes.TAILLE_CASE)
                if rect.collidepoint(mouse):
                    if case == 0:
                        self.posG = (indL, indC)
                        self.forceRebon = Constantes.DICT_FORCE_REBON[indL]
                        self.posL = Constantes.POS_GRILLE_Y + (Constantes.TAILLE_CASE + Constantes.ESPACE_CASE) * indL + 1
                        self.posObjX = Constantes.POS_GRILLE_X + (Constantes.TAILLE_CASE + Constantes.ESPACE_CASE) * indC + 1
                        self.posObjY = 0
                        self.chute = True
                        if self.joueur == 0:
                            self.joueur = 1
                        else:
                            self.joueur = 0
    
    def MenuDeDemarage(self):

        while self.etat == "Menu":

            self.screen.fill("black")

            pygame.draw.rect(self.screen, (255, 255, 255), self.boutonJouer)
            pygame.draw.rect(self.screen, (255, 255, 255), self.boutonQuitter)

            play_text = self.font.render("Jouer", True, (0, 0, 0))
            quit_text = self.font.render("Quitter", True, (0, 0, 0))

            self.screen.blit(play_text, ((800-140)/2 + 25, (600 - 50)/2 - 35 + 7))
            self.screen.blit(quit_text, ((800-140)/2 + 10, (600 - 50)/2 - 35 + 80))

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
        self.posObjY += self.gravity
        self.gravity += 1
        
        if self.joueur == 1:
            self.screen.blit(self.jetonRouge, (self.posObjX, self.posObjY))
        else:
            self.screen.blit(self.jetonJaune, (self.posObjX, self.posObjY))
        if self.posObjY >= self.posL - self.gravity:
            self.gravity = self.forceRebon
            self.forceRebon /= 2
            if abs(self.forceRebon) <= 0.1:
                self.chute = False
                Constantes.GRILLE[self.posG[0]][self.posG[1]] = 2 if self.joueur == 0 else 1
                self.forceRebon = -5


Ui().MenuDeDemarage()