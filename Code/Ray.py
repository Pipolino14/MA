import pygame
import math

from Rotator import *
from Globals import *

# Diese Klasse generiert einen einzelnen Sichstrahl, der Kollisionen mit einer bestimmte 
# Gruppe detektiert und die Distanz zwischen das Tier wo diesen Strahl "besitzt" (Wirt-Tier)
# und ein Tier der gesehene Gruppe zurückgibt
class Ray(pygame.sprite.Sprite):
    def __init__(self, animal, surface, view_range, angle_offset):
        pygame.sprite.Sprite.__init__(self)
        self.animal = animal
        self.surface = surface
        self.angle_offset = angle_offset
        self.view_range = view_range
        self.image = Rotator.get_image(animal)
        self.image.set_colorkey((255, 0, 0))  # Rot ist als Transparente Farbe gesetzt
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.distance = 0

    # Checkt ob man ein Tier in einer Gruppe sieht (Hunter oder Prey) und aktualisiert die 
    # Distanz zu dem Tier
    def checkSeeAnimal(self, own_pos, animal_Group):
        if pygame.sprite.spritecollide(self, animal_Group, False, None):
            spriteGroup = pygame.sprite.spritecollide(
                self, animal_Group, False, pygame.sprite.collide_mask
            )
            if len(spriteGroup) > 0:
                other_pos = (spriteGroup[0].x, spriteGroup[0].y)
                dist = math.dist(own_pos, other_pos)
                if dist <= self.view_range:
                    #Hier werden die gesehene Tiere angezeigt
                    if Globals.show_target:
                        see_Color = (0, 0, 255)
                        if (self.animal == "prey"):
                            see_Color = (0, 255, 255)
                        pygame.draw.line(self.surface, see_Color, own_pos, other_pos, 1)
                    norm_dist = dist/self.view_range
                    inv_norm_dist = 2 * (1 - norm_dist)
                    net_dist = inv_norm_dist - 1
                    self.distance = net_dist
                else:
                    self.distance = 0
            else:
                self.distance = 0
    
    #Update funktion. Definiert die Maske immer wieder je nach Position und Winkel des "Wirt-Tieres" 
    def update(self, pos, angle, animal_group):
        self.image.fill((255, 0, 0))  # Mit rot ausfüllen, rot ist für rays Transparent
        #Das ist um die vision Rays anzuzeigen.
        if Globals.show_ray:
            radians = math.radians(angle + self.angle_offset)
            self.yy = math.cos(radians) * self.view_range
            self.xx = math.sin(radians) * self.view_range
            pygame.draw.line(self.surface, (150, 150, 150, 0), pos, (pos[0] - self.xx, pos[1] - self.yy),1)

        #Nun die Maske laden, um dort Kollisionen zu sehen
        self.mask = Rotator.get_mask(self.animal, angle + self.angle_offset)
        self.rect.center = pos
        self.checkSeeAnimal(pos, animal_group)