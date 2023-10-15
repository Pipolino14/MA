import pygame
import random
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
    def __init__(self, surface):
        self.POSX = random.randint(100, 1900)
        self.POSY = random.randint(100, 1000)
        self.START_POS = (self.POSX, self.POSY)
        self.STRTvel = random.randint(1, 3)
        self.STRTangle = random.randint(0, 360)
        self.Angle_SPD = random.randint(1, 10)
        self.FOV = math.pi / 4
        #self.STRTangle = 0
        Animal.__init__(self, surface)

    def update(self, *args: Any, **kwargs: Any):
        self.Energy = self.Energy - 1
        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)
        Animal.update(self)
    
    def recharge(self):
        self.Energy = 600
