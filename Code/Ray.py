from typing import Any
import pygame
import math
from utils import *


# Diese Klasse generiert einen einzelnen Sichstrahl, der Collisionen mit einer bestimmte 
# Gruppe detektiert und die Distanz zwischen das Tier wo diesen Strahl "besitzt" (Wirt-Tier)
# und ein Tier der gesehene Gruppe an eine callback Funktion zurückgibt
class Ray(pygame.sprite.Sprite):
    def __init__(self, surface, view_range, angle_offset):
        pygame.sprite.Sprite.__init__(self)
        self.surface = surface
        self.angle_offset = angle_offset
        self.view_range = view_range
        self.rect_size = 2 * view_range
        self.image = pygame.Surface([self.rect_size, self.rect_size])
        self.image.set_colorkey((255, 0, 0))  # Rot ist als Transparente Farbe gesetzt
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

    # Checkt ob man ein Tier in einer Gruppe sieht (Hunter oder Prey) und gibt die 
    # Distanz weiter an eine Callback Funktion
    def checkSeeAnimal(self, index, hunterPos, animalGroup, callback):
        if pygame.sprite.spritecollide(self, animalGroup, False, None):
            spriteGroup = pygame.sprite.spritecollide(
                self, animalGroup, False, pygame.sprite.collide_mask
            )
            if len(spriteGroup) > 0:
                preyPos = (spriteGroup[0].x, spriteGroup[0].y)
                dist = math.dist(hunterPos, preyPos)
                callback(index, dist)
            else:
                callback(index, 0)

    #Update funktion. Definiert die Maske immer wieder je nach Position und Winkel des "Wirt-Tieres" 
    def update(self, x, y, angle):
        self.image.fill((255, 0, 0))  # Mit rot ausfüllen, rot ist für rays Transparent
        radians = math.radians(angle + self.angle_offset)
        yy = math.cos(radians) * self.view_range
        xx = math.sin(radians) * self.view_range
        pygame.draw.line(
            self.image,
            (255, 0, 255),
            (self.view_range, self.view_range),
            (self.view_range - xx, self.view_range - yy),
            1,
        )
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)