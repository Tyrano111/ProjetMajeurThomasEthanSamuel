#Il s'occupe de toute la partie graphique avec pygame
import pygame
import ConstantesEtVariable as CV
import Game

class Jeton:
    def __init__(self, couleur):
        self.couleur = couleur
        self.uiJeton = pygame.image.load("Assets/JetonJaune.png").convert_alpha() if couleur == "j" else pygame.image.load("Assets/JetonRouge.png").convert_alpha()
        self.position = [11, 0]
        self.gravite = 2

    def draw(self, ecran):
        ecran.blit(self.uiJeton, (self.position[0], self.position[1]))

    def rebon(self, ecran, positionFinal, forceRebon):
        peut_rebondir = True
        self.position[0] = positionFinal[0] + 11
        self.position[1] += self.gravite
        self.gravite += 1

        self.draw(ecran)
        if self.position[1] >= positionFinal[1] - self.gravite + 11:
            self.gravite = forceRebon
            forceRebon /= 2
            if abs(forceRebon) <= 0.1:
                peut_rebondir = False
                self.gravite = 2
        if peut_rebondir:
            return forceRebon
        return 0

class Bouton:
    def __init__(self, position, taille, asset):
        self.position = position
        self.uiBouton = pygame.image.load(asset).convert_alpha()
        self.rectBouton = pygame.Rect(position[0], position[1], taille[0], taille[0])

    def draw(self, ecran):
        ecran.blit(self.uiBouton, self.position)

    def est_clique(self, mouse):
        return True if self.rectBouton.collidepoint(mouse) else False


class BoutonRond:
    def __init__(self, position, diametre, asset):
        self.position = position  # coin haut-gauche de l'image
        self.rayon = diametre / 2
        self.centre = (position[0] + self.rayon, position[1] + self.rayon)
        self.uiBouton = pygame.image.load(asset).convert_alpha()

    def draw(self, ecran):
        ecran.blit(self.uiBouton, self.position)

    def est_clique(self, mouse):
        dx = mouse[0] - self.centre[0]
        dy = mouse[1] - self.centre[1]
        return dx * dx + dy * dy <= self.rayon * self.rayon

class Grille:
    def __init__(self):
        self.uiCase = pygame.image.load("Assets/CaseGrille.png").convert_alpha()
        self.position = (CV.POS_GRILLE_X, CV.POS_GRILLE_Y)
        self.uiJetonJaune = pygame.image.load("Assets/JetonJaune.png").convert_alpha()
        self.uiJetonRouge = pygame.image.load("Assets/JetonRouge.png").convert_alpha()

    def draw(self, ecran):
        for indLigne, ligne in enumerate(CV.grille):
            posLigne = self.position[1] + indLigne * CV.TAILLE_CASE
            for indColone, case in enumerate(ligne):
                posColone = self.position[0] + indColone * CV.TAILLE_CASE
                if case != "":
                    ecran.blit(self.uiJetonRouge, (posColone + 11, posLigne + 11)) if case == "r" else ecran.blit(self.uiJetonJaune, (posColone + 11, posLigne + 11)) 
                ecran.blit(self.uiCase, (posColone, posLigne))
                    
class Menu:
    def __init__(self, typeMenu):
        self.Bouton1 = Bouton((300, 300), (300, 150), "Assets/BoutonJouer.png") if typeMenu == "Accueil" else Bouton((300, 300), (300, 150), "Assets/BoutonJouer.png")
        self.Bouton2 = Bouton((300, 600), (300, 150), "Assets/BoutonJouer.png") if typeMenu == "Accueil" else Bouton((300, 600), (300, 150), "Assets/BoutonJouer.png")

    def draw(self, ecran):
        self.Bouton1.draw(ecran)
        self.Bouton2.draw(ecran)

    def BoutonClique(self, mouse):
        if self.Bouton1.est_clique(mouse):
            return 1
        elif self.Bouton2.est_clique(mouse):
            return 2
        return 0


