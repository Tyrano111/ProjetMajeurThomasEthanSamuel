import pygame
import random

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # Vitesse aléatoire en X et Y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.radius = random.randint(3, 6)
        self.lifetime = 30  # Nombre de frames avant de disparaître
        self.color = (255, 165, 0) # Orange

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)