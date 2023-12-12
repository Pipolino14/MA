import pygame
import random
import copy
from Animal import *
from utils import *

#Image and the corresponding mask of the image for collision
HUNTER_IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), 0.5)
HUNTER_MASK = pygame.mask.from_surface(HUNTER_IMG)

class HunterAnimal(Animal):
    IMG = HUNTER_IMG
    IMGHEI = HUNTER_IMG.get_height()
    IMGWID = HUNTER_IMG.get_height()
    MASK = HUNTER_MASK
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
        self.Angle_SPD = random.randint(5, 10)
        self.fitness = 0
        #self.FOVdis = 30
        self.seen = 0
        self.surface = surface
        self.Energy = 1200

    
        #self.STRTangle = 0
        Animal.__init__(self, surface, rays=5, FOV=60, ROV=300)

        #Distanzenliste für die Rays im Raycasting
        self.distances = [0, 0, 0, 0, 0]

    def deepcopy(self):
        # print(self.weights)
        # rngweights = np.dot(self.weights[0], np.random.randn(5, 4)) + np.dot(self.weights[1], np.random.randn(4, 2))
        # print(rngweights)
        # rngbiases = self.biases * [np.random.randn(4), np.random.randn(2)]
        copyhunter = HunterAnimal(self.surface, self.x, self.y)
        return copyhunter
    
    def seePrey(self, index, distance):
        self.distances[index] = round(distance, 2)
        if sum(self.distances) > 0:
            #macht alle rays sichtbar, falls der hunter etwas sieht

            print(self.distances)
            self.rayGroup.draw(self.surface)
            
            self.Network.forward(self.distances)

            if self.Network.forward(self.distances)[0] < 0.33:
                self.rotate(left=True)
            elif self.Network.forward(self.distances)[0] > 0.66:
                self.rotate(right=True)
            if self.Network.forward(self.distances)[1] > 0.66:
                self.increase_speed(0.1)
            elif self.Network.forward(self.distances)[1] < 0.33:
                self.reduce_speed(0.1)
    


    def recharge(self):
        self.Energy = self.Energy + 600


    def update(self, preyGroup, *args: Any, **kwargs: Any):
        if self.vel <= 3:
            self.vel = 3

        Animal.update(self)

        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)
        print(self.distances, self.x, self.y, len(self.rayGroup.sprites()))
        for (index, ray) in enumerate(self.rayGroup.sprites()):
            ray.checkSeeAnimal(index, (self.x, self.y), preyGroup, self.seePrey)
    
    