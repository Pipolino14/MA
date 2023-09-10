import pygame
import random
from Animal import *
from utils import *

#Image and the corresponding mask of the image for collision
PREY_IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), 1)
PREY_MASK = pygame.mask.from_surface(PREY_IMG)


class PreyAnimal(Animal):
    IMG = PREY_IMG
    MASK = PREY_MASK
    START_POS = (500, 500)
    IMGHEI = PREY_IMG.get_height()
    IMGWID = PREY_IMG.get_height()
    def __init__(self):
        self.POSX = random.randint(100, 1900)
        self.POSY = random.randint(100, 1000)
        self.START_POS = (self.POSX, self.POSY)
        self.STRTvel = random.randint(1, 3)
        self.STRTangle = random.randint(0, 360)
        self.Angle_SPD = random.randint(1, 10)
        #self.STRTangle = 0
        Animal.__init__(self)