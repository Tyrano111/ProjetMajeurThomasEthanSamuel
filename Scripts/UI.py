#Il s'occupe de toute la partie graphique avec pygame
import pygame
import ConstantesEtVariable as CV

class Jeton:
    def __init__(self):
        self.uiJetonJaune = pygame.image.load("Assets/JetonJaune.png").convert_alpha()
        self.uiJetonRouge = pygame.image.load("Assets/JetonRouge.png").convert_alpha()
        self.uiJetonnNoir = pygame.image.load("Assets/JetonNoir.png").convert_alpha()
        self.position = [11, 0]
        self.gravite = 2

    def draw(self, ecran, couleur):
        if couleur == "j":
            ecran.blit(self.uiJetonJaune, (self.position[0], self.position[1]))
        elif couleur == "r":
            ecran.blit(self.uiJetonRouge, (self.position[0], self.position[1]))
        else: 
            ecran.blit(self.uiJetonnNoir, (self.position[0], self.position[1]))

    def rebon(self, ecran, positionFinal, forceRebon, couleur):
        peut_rebondir = True
        self.position[0] = positionFinal[0] + 11
        self.position[1] += self.gravite
        self.gravite += 1

        self.draw(ecran, couleur)
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
        self.rectBouton = pygame.Rect(position[0], position[1], taille[0], taille[1])

    def draw(self, ecran):
        ecran.blit(self.uiBouton, self.position)

    def est_clique(self, mouse):
        return True if self.rectBouton.collidepoint(mouse) else False


class BoutonSort:
    def __init__(self, position, diametre, asset):
        self.position = position  # coin haut-gauche de l'image
        self.rayon = diametre / 2
        self.centre = (position[0] + self.rayon, position[1] + self.rayon)
        self.uiBouton = pygame.image.load(asset + ".png").convert_alpha()
        self.uiBoutonClique = pygame.image.load(asset + "Clique.png").convert_alpha()
        self.uiBoutonUtilise = pygame.image.load(asset + "Utilise.png").convert_alpha()

    def draw(self, ecran, etat):
        if etat == "Normal":
            ecran.blit(self.uiBouton, self.position)
        elif etat == "Clique":
            ecran.blit(self.uiBoutonClique, self.position)
        else:
            ecran.blit(self.uiBoutonUtilise, self.position)

    def est_clique(self, mouse):
        dx = mouse[0] - self.centre[0]
        dy = mouse[1] - self.centre[1]
        return dx * dx + dy * dy <= self.rayon * self.rayon

class Grille:
    def __init__(self):
        self.uiCase = pygame.image.load("Assets/CaseGrille.png").convert_alpha()
        self.uiCaseSurvole = pygame.image.load("Assets/CaseGrilleSurvole.png").convert_alpha()
        self.uiCaseBloque = pygame.image.load("Assets/CaseBloque.png").convert_alpha()
        self.position = (CV.POS_GRILLE_X, CV.POS_GRILLE_Y)
        self.uiJetonJaune = pygame.image.load("Assets/JetonJaune.png").convert_alpha()
        self.uiJetonRouge = pygame.image.load("Assets/JetonRouge.png").convert_alpha()
        self.uiJetonNoir = pygame.image.load("Assets/JetonNoir.png").convert_alpha()
        self.uiJetonFantomeJaune = pygame.image.load("Assets/JetonFantomeJaune.png").convert_alpha()
        self.uiJetonFantomeRouge = pygame.image.load("Assets/JetonFantomeRouge.png").convert_alpha()
        self.fontTexte = pygame.font.SysFont("Corbel", 35, bold=True)

    def draw(self, grille, ecran, mouse, useSpell, joueur):
        bloque = None
        for indLigne, ligne in enumerate(grille):
            posLigne = self.position[1] + indLigne * CV.TAILLE_CASE
            for indColone, case in enumerate(ligne):
                if case == ".j" or case == ".r":
                    bloque = indColone
                posColone = self.position[0] + indColone * CV.TAILLE_CASE
                if case != " " and case != ".j" and case != ".r":
                        if case == "r":
                            ecran.blit(self.uiJetonRouge, (posColone + 11, posLigne + 11))
                        elif case == "j":
                            ecran.blit(self.uiJetonJaune, (posColone + 11, posLigne + 11))
                        elif case == "n":
                            ecran.blit(self.uiJetonNoir, (posColone + 11, posLigne + 11)) 
                        elif case == "fj":
                            ecran.blit(self.uiJetonFantomeJaune, (posColone + 11, posLigne + 11))
                        else:
                            ecran.blit(self.uiJetonFantomeRouge, (posColone + 11, posLigne + 11))
                if useSpell:
                    rect = pygame.Rect(posColone, posLigne, CV.TAILLE_CASE, CV.TAILLE_CASE)
                else:
                    rect = pygame.Rect(posColone, CV.POS_GRILLE_Y, CV.TAILLE_CASE, CV.TAILLE_GRILLE[1])
                if indColone == bloque:
                    ecran.blit(self.uiCaseBloque, (posColone, posLigne))
                elif rect.collidepoint(mouse):
                    ecran.blit(self.uiCaseSurvole, (posColone, posLigne))
                else:
                    ecran.blit(self.uiCase, (posColone, posLigne))
        titre = self.fontTexte.render("Tour du Joueur :", True, (255, 255, 255))
        rectTitre = titre.get_rect(center=(1065, 50))
        ecran.blit(titre, rectTitre)
        
        ecran.blit(self.uiJetonRouge, (1200, 1)) if joueur == "r" else ecran.blit(self.uiJetonJaune, (1200, 1))
                    
class Menu:
    def __init__(self, typeMenu):
        self.boutonVsIA = Bouton((550, 200), (200, 120), "Assets/BoutonVsIA.png")
        self.boutonJcJ = Bouton((550, 400), (200, 120), "Assets/BoutonJcJ.png")
        self.boutonQuitter = Bouton((550, 600), (200, 90), "Assets/BoutonQuitter.png")

    def draw(self, ecran):
        self.boutonVsIA.draw(ecran)
        self.boutonJcJ.draw(ecran)
        self.boutonQuitter.draw(ecran)

    def BoutonClique(self, mouse):
        if self.boutonVsIA.est_clique(mouse):
            return 1
        elif self.boutonJcJ.est_clique(mouse):
            return 2
        elif self.boutonQuitter.est_clique(mouse):
            return 3
        return 0

class Victoire:
    def __init__(self):
        self.fontTitre = pygame.font.SysFont("Corbel", 80, bold=True)
        self.fontJoueur = pygame.font.SysFont("Corbel", 55, bold=True)
        self.fontTexte = pygame.font.SysFont("Corbel", 30)

        self.couleurTexte = (255, 255, 255)
        self.couleurRouge = (220, 40, 40)
        self.couleurJaune = (240, 210, 30)

        self.boutonMenu = Bouton((605, 500), (90, 90), "Assets/BoutonAccueil.png")

    def draw(self, ecran, joueur):

        # Titre
        titre = self.fontTitre.render("VICTOIRE !", True, self.couleurTexte)
        rectTitre = titre.get_rect(center=(ecran.get_width() // 2, 150))
        ecran.blit(titre, rectTitre)

        # Nom du joueur gagnant
        if joueur == "r":
            nomJoueur = "Joueur rouge"
            couleurJoueur = self.couleurRouge
        else:
            nomJoueur = "Joueur jaune"
            couleurJoueur = self.couleurJaune

        texteJoueur = self.fontJoueur.render(nomJoueur, True, couleurJoueur)
        rectJoueur = texteJoueur.get_rect(center=(ecran.get_width() // 2, 280))
        ecran.blit(texteJoueur, rectJoueur)

        # Texte complémentaire
        texteFin = self.fontTexte.render("a remporté la partie !", True, self.couleurTexte)
        rectFin = texteFin.get_rect(center=(ecran.get_width() // 2, 350))
        ecran.blit(texteFin, rectFin)

        self.boutonMenu.draw(ecran)
