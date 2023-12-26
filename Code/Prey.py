import pygame
import random
from Animal import *
from utils import *

class PreyAnimal(Animal):
    IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), 0.5)
    MASK = pygame.mask.from_surface(IMG)
    IMGHEI = IMG.get_height()
    IMGWID = IMG.get_height()
    def __init__(
        self,
        surface,
        posX = None,
        posY = None
        ):
        self.POSX = posX
        if posX == None:
            posX = random.randint(0, WIDTH)
        self.POSY = posY
        if posY == None:
            posY = random.randint(0, HEIGHT)
        self.START_POS = (posX, posY)
        self.STRTvel = random.randint(0, 1)
        self.STRTangle = random.randint(0, 360)
        self.Angle_SPD = random.randint(3, 7)
        self.fitness = 0
        self.Energy = 600
        
        Animal.__init__(self, "prey", surface, rays=5, FOV=270, ROV=150)

        self.distances = [-1, -1, -1, -1, -1]

    def deepcopy(self):
        newprey = PreyAnimal(self.surface, self.x, self.y)
        return newprey

    def recharge(self):
        if self.vel <=0:
            self.Energy += 0.5
    
    def turningGraph(self, x):
        x = (4 * (x - 0.5)**2)**2
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
            #print(netResult)
            #print("H:",netResult)
            #print(netResult[0], netResult[1])

            #Option 1: der Wert benutzen um mehr oder weniger zu drehen, gedrittelt
            if (netResult[0] < 0.5):
                self.rotate(turn_right=False, turn_angle=ResultTurn)
            if (netResult[0] > 0.5):
                self.rotate(turn_right=True, turn_angle=ResultTurn)

            #Speed:
            if netResult[1] > 0.5:
                self.increase_speed(ResultSpeed * 0.2)
            elif netResult[1] < 0.5:
                self.reduce_speed(ResultSpeed * 0.2)

    def update(self, hunterGroup):
        if self.Energy >= 0:
            self.recharge()
        
        self.distances = Animal.update(self, hunterGroup)
        self.avoid()