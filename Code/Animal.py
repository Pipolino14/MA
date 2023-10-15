from typing import Any

import pygame
import math
from utils import *

BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()


class Animal(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.IMG
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
        self.mask = self.MASK
        self.vel = self.STRTvel
        self.acceleration = 0.3
        self.angle = math.radians(self.STRTangle)
        self.angle_speed = self.Angle_SPD
        self.x, self.y = self.START_POS
        self.Energy = 600
        self.surface = surface
        self.halfFOV = self.FOV / 2
        #self.id = id
    
    def rotate(self, left=False, right=False):
        if left==True:
            self.angle += self.angle_speed
        if right==True:
            self.angle -= self.angle_speed

    def move(self):
        #converting the current facing angle to RAD
        radians = math.radians(self.angle)
        #cos(RichtungsWinkel) * Hypothenuse{velocity vector} = Gegenkatethe --> Y movement
        vertical = math.cos(radians) * self.vel
        #sin(RichtungsWinkel) * Hypothenuse{velocity vector} = Ankatethe --> X movement
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def increase_speed(self, inc):
        self.vel = self.vel + inc
    
    def reduce_speed(self, red):
        self.vel = max(self.vel - red, 0)
    

    #proof of concept for vision-rays
    def visionray(self):
        faceangle =- math.radians(self.angle)
        pygame.draw.line(self.surface, (255, 0, 0), (self.x, self.y), (self.x + math.sin(faceangle) * 100, self.y - math.cos(faceangle) * 100), 1)

        pygame.draw.line(self.surface, (0, 255, 0), (self.x, self.y),
                                       (self.x + math.sin(faceangle - self.halfFOV) * 100,
                                        self.y - math.cos(faceangle - self.halfFOV) * 100), 1)

        pygame.draw.line(self.surface, (0, 255, 0), (self.x, self.y),
                                       (self.x + math.sin(faceangle + self.halfFOV) * 100,
                                        self.y - math.cos(faceangle + self.halfFOV) * 100), 1)


#    def draw(self, win):
#        blit_rotate_center(win, self.image, (self.x, self.y), (self.angle+90))


    def collision(self, mask, x=0, y=0):
        animal_mask = pygame.mask.from_surface(self.image)
        offset = (int(self.x - x), int(self.y - y))
        touch = mask.overlap(animal_mask, offset)
        return touch
    

    def check_border(self):
        HEI = (self.IMG.get_height()/2)
        WID = (self.IMGWID/2)
        #bottom
        if self.y > HEIGHT - HEI:
            self.angle = (360 - self.angle) + 180
            self.y = HEIGHT - HEI - 1
        #top
        if self.y < HEI:
            self.angle = (360 - self.angle) + 180
            self.y = HEI + 1
        #right
        if self.x > WIDTH - WID:
            self.angle = (360 - self.angle) 
            self.x = WIDTH - WID - 1
        #left
        if self.x < WID:
            self.angle = (360 - self.angle) 
            self.x = WID + 1
        


    def update(self, *args: Any, **kwargs: Any) -> None:
        #self.rect.move_ip(0, 1)
        self.move()
        self.check_border()
        self.visionray()
        if self.vel < 0:
            self.vel = 0
        self.rect.center=(self.x, self.y)
        print(self.angle)

        

