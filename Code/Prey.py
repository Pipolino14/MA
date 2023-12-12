import pygame
import random
from Animal import *
from utils import *

#Image and the corresponding mask of the image for collision
PREY_IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), 0.5)
PREY_MASK = pygame.mask.from_surface(PREY_IMG)


class PreyAnimal(Animal):
    IMG = PREY_IMG
    MASK = PREY_MASK
    START_POS = (500, 500)
    IMGHEI = PREY_IMG.get_height()
    IMGWID = PREY_IMG.get_height()
    def __init__(
        self,
        surface,
        posX = None,
        posY = None
        ):
        self.POSX = posX
        if posX == None:
            posX = random.randint(100, 1900)
        self.POSY = posY
        if posY == None:
            posY = random.randint(100, 1000)
        self.START_POS = (posX, posY)
        self.STRTvel = random.randint(1, 3)
        self.STRTangle = random.randint(0, 360)
        self.Angle_SPD = random.randint(3, 7)
        self.fitness = 0
        self.Energy = 600
        
        Animal.__init__(self, surface, rays=5, FOV=270, ROV=150)

        self.distances = [0, 0, 0, 0, 0]

    def deepcopy(self):
        newprey = PreyAnimal(self.surface, self.x, self.y)
        return newprey

    def recharge(self):
        if self.vel <=0:
            self.Energy += 0.5

    def seeHunter(self, index, distance):
        self.distances[index] = round(distance, 2)
        if sum(self.distances) > 0:
            #macht alle rays sichtbar, falls der hunter etwas sieht
            self.rayGroup.draw(self.surface)
            #führt die forward Funktion im Neuralen Netzwerk aus, sobald die Rays etwas sehen.
            self.Network.forward(self.distances)
            #entscheidet, welche Richtung es gehen will.
            if self.Network.forward(self.distances)[0] < 0.33:
                self.rotate(left=True)
            elif self.Network.forward(self.distances)[0] > 0.66:
                self.rotate(right=True)
            if self.Network.forward(self.distances)[1] > 0.5:
                self.increase_speed(0.1)
        else:
            self.reduce_speed(0.1)


    def update(self, hunterGroup, *args: Any, **kwargs: Any):
        if self.Energy >= 0:
            self.recharge()
        
        Animal.update(self)
        for index, ray in enumerate(self.rayGroup.sprites()):
            ray.checkSeeAnimal(index, (self.x, self.y), hunterGroup, self.seeHunter)