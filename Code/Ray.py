from typing import Any
import pygame
import math
from utils import *


# Diese Klasse generiert einen einzelnen Sichstrahl, der Collisionen mit einer bestimmte 
# Gruppe detektiert und die Distanz zwischen das Tier wo diesen Strahl "besitzt" (Wirt-Tier)
# und ein Tier der gesehene Gruppe an eine callback Funktion zurückgibt
class Ray(pygame.sprite.Sprite):
    def __init__(self, animal, surface, view_range, angle_offset):
        pygame.sprite.Sprite.__init__(self)
        self.animal = animal
        self.surface = surface
        self.angle_offset = angle_offset
        self.view_range = view_range
        self.rect_size = 2 * view_range
        self.image = pygame.Surface([self.rect_size, self.rect_size])
        self.image.set_colorkey((255, 0, 0))  # Rot ist als Transparente Farbe gesetzt
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.distance = -1

    # Checkt ob man ein Tier in einer Gruppe sieht (Hunter oder Prey) und gibt die 
    # Distanz weiter an eine Callback Funktion
    def checkSeeAnimal(self, own_pos, animal_Group):
        if pygame.sprite.spritecollide(self, animal_Group, False, None):
            spriteGroup = pygame.sprite.spritecollide(
                self, animal_Group, False, pygame.sprite.collide_mask
            )
            if len(spriteGroup) > 0:
                other_pos = (spriteGroup[0].x, spriteGroup[0].y)
                dist = math.dist(own_pos, other_pos)
                see_Color = (0, 0, 255)
                if (self.animal == "prey"):
                    see_Color = (0, 255, 255)

                pygame.draw.line(self.surface, see_Color, own_pos, other_pos, 1)

                #if dist > self.view_range:
                #    dist = self.view_range

                norm_dist = dist/self.view_range
                inv_norm_dist = 2 * (1 - norm_dist)
                net_dist = inv_norm_dist - 1
                self.distance = net_dist
            else:
                self.distance = -1
    
    #Update funktion. Definiert die Maske immer wieder je nach Position und Winkel des "Wirt-Tieres" 
    def update(self, pos, angle, animal_group):
        self.image.fill((255, 0, 0))  # Mit rot ausfüllen, rot ist für rays Transparent
        radians = math.radians(angle + self.angle_offset)
        self.yy = math.cos(radians) * self.view_range
        self.xx = math.sin(radians) * self.view_range
        self.rect.center = pos
        self.checkSeeAnimal(pos, animal_group)