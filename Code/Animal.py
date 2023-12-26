from typing import Any
import pygame
import math
from utils import *
from Ray import *
from Network import *

BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BG_IMG = BG_IMG.convert()
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
pygame.display.set_caption("Calculating of the fittest")

MatrixLimit = 0.5

class Animal(pygame.sprite.Sprite):
    def __init__(self, animal, surface, rays, FOV, ROV):
        pygame.sprite.Sprite.__init__(self)
        self.image = self.IMG
        self.rect = self.image.get_rect()
        self.rect.center = (300, 300)
        self.mask = self.MASK
        self.vel = self.STRTvel
        self.acceleration = 0.3
        self.angle = self.STRTangle
        #self.angle = math.radians(self.STRTangle)
        self.angle_speed = self.Angle_SPD
        self.x, self.y = self.START_POS
        self.surface = surface
        self.generation = 0
        self.rayGroup = pygame.sprite.Group()
        self.weights = [np.random.uniform(0, MatrixLimit, size=(5, 4)), np.random.uniform(0, MatrixLimit, size=(4, 2))]
        self.biases = [np.random.uniform(0, MatrixLimit, size=(1, 4)), np.random.uniform(0, MatrixLimit, size=(1, 2))]
        self.Network = Network(self.weights, self.biases)

        


        for ray in range(rays):
            rayAngle = ray * (FOV / rays) - round(FOV / 2, 0) + ((FOV / rays) / 2)
            ray = Ray(animal, surface, ROV, rayAngle)
            self.rayGroup.add(ray)

        self.id = id
    
    def newgen(self):
        self.generation = self.generation + 1
    
    # def rotate(self, turnspeed, left=False, right=False):
    #     if left==True:
    #         self.angle += self.angle_speed * turnspeed
    #     if right==True:
    #         self.angle -= self.angle_speed * turnspeed
        
    def rotate(self, turn_right, turn_angle):
        angle_factor = 30
        if turn_right:
            self.angle += angle_factor * turn_angle
        else:
            self.angle -= angle_factor * turn_angle

    def move(self):
        #converting the current facing angle to RAD
        radians = math.radians(self.angle)
        #cos(RichtungsWinkel) * Hypothenuse{velocity vector} = Gegenkatethe --> Y movement
        vertical = math.cos(radians) * self.vel
        #sin(RichtungsWinkel) * Hypothenuse{velocity vector} = Ankatethe --> X movement
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

        #berechnet die verbrauchte Energie bei der immomentigen Geschwindigkeit
        self.Energy = self.Energy - self.vel

    def increase_speed(self, inc):
        self.vel = min(self.vel + inc, 5)
    
    def reduce_speed(self, red):
        self.vel = max(self.vel - red, 0)
    
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
        
    def rayupdate(self):
        for ray in self.rayGroup.sprites():
            ray.update(self.x, self.y, self.angle)

    def visionray(self):
        faceangle =- math.radians(self.angle)
        pygame.draw.line(self.surface, (255, 0, 0), (self.x, self.y), (self.x + math.sin(faceangle) * 100, self.y - math.cos(faceangle) * 100), 2)


    def update(self, target_group) -> None:
        self.move()
        self.check_border()

        #with Pool() as pool:
        #    pool.imap_unordered(self.rayupdate, self.rayGroup.sprites())

        if self.vel < 0:
            self.vel = 0
        self.rect.center=(self.x, self.y)

        self.rayGroup.update((self.x, self.y), self.angle, target_group)
        distances = []
        for ray in self.rayGroup.sprites():
            distances.append(ray.distance)
        self.visionray()
        return distances
        

        

        

