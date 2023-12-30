import pygame
import random
from Animal import *
from utils import *
from Globals import *

class PreyAnimal(Animal):
    def __init__(
        self,
        surface,
        posX = None,
        posY = None
        ):
        self.IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), Globals.animal_size)
        self.MASK = pygame.mask.from_surface(self.IMG)
        self.IMGHEI = self.IMG.get_height()
        self.IMGWID = self.IMG.get_height()
        self.POSX = posX
        if posX == None:
            posX = random.randint(0, WIDTH)
        self.POSY = posY
        if posY == None:
            posY = random.randint(0, HEIGHT)
        self.START_POS = (posX, posY)
        #self.STRTvel = random.randint(0, 1)
        #self.STRTangle = random.randint(0, 360)
        #self.Angle_SPD = random.randint(3, 7)
        self.fitness = random.randint(0, 100)
        self.Energy = Globals.prey_energy
        
        Animal.__init__(self, "prey", surface, rays=5, FOV=Globals.PREY_FOV, ROV=Globals.PREY_ROV)

        self.distances = [-1, -1, -1, -1, -1]

    def deepcopy(self):
        newprey = PreyAnimal(self.surface, self.x, self.y)
        newprey.newgen()
        return newprey

    def recharge(self):
        if self.vel <=0:
            self.Energy += 0.5
    
    def turningGraph(self, x):
        x = (4 * (x - 0.5)**2)**1
        return x

    #def seeHunter(self, index, distance):
    #    self.distances[index] = round(distance, 2)
        
    def avoid(self):
        if(True): # max(self.distances)> -1
            # macht alle rays sichtbar, falls der hunter etwas sieht
            self.rayGroup.draw(self.surface)
            # führt die forward Funktion im Neuralen Netzwerk aus, sobald die Rays etwas sehen.
            netResult = self.Network.forward(self.distances)
            ResultTurn = self.turningGraph(netResult[0])
            ResultSpeed = self.turningGraph(netResult[1])

            #Option 1: der Wert benutzen um mehr oder weniger zu drehen, gedrittelt
            if (netResult[0] < 0.5):
                self.rotate(turn_right=False, turn_angle=ResultTurn)
                
            if (netResult[0] > 0.5):
                self.rotate(turn_right=True, turn_angle=ResultTurn)

            #Speed:
            if netResult[1] > 0.5:
                self.increase_speed(ResultSpeed)
            elif netResult[1] < 0.5:
                self.reduce_speed(ResultSpeed)

    def update(self, hunterGroup):
        if self.Energy >= 0:
            self.recharge()
        
        for index, ray in enumerate(self.rayGroup.sprites()):
            self.distances[index] = -1

        self.distances = Animal.update(self, hunterGroup)
        self.avoid()