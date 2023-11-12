import pygame
import random
import copy
from Animal import *
from utils import *

#Image and the corresponding mask of the image for collision
HUNTER_IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), 1)
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
    
        #self.STRTangle = 0
        Animal.__init__(self, surface, rays=5, FOV=45, ROV=200)

        #Distanzenliste für die Rays im Raycasting
        self.distances = [0, 0, 0, 0, 0]

    def deepcopy(self):
        copyhunter = HunterAnimal(self.surface, self.x, self.y)
        return copyhunter
    
    def seePrey(self, index, distance):
        self.distances[index] = round(distance, 2)
        if sum(self.distances) > 0:
            #macht alle rays sichtbar, falls der hunter etwas sieht
            self.rayGroup.draw(self.surface)
            print("Hunter:", self.distances)
            #Die resultierende self.distances Liste wird der Input Layer im NW sein


    def update(self, preyGroup, *args: Any, **kwargs: Any):
        self.Energy = self.Energy - 1

        for (index, ray) in enumerate(self.rayGroup.sprites()):
            ray.checkSeeAnimal(index, (self.x, self.y), preyGroup, self.seePrey)
        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)
        Animal.update(self)
    
    def recharge(self):
        self.Energy = self.Energy + 50
