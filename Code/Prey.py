#import pygame
import random
from Animal import *
from utils import *
from Globals import *

class PreyAnimal(Animal):
    def __init__(self,surface,posX = None,posY = None):
        self.fitness = random.randint(0, 100)
        self.Energy = Globals.prey_energy
        
        Animal.__init__(self, "prey", surface, posX, posY, rays=5,
                        FOV=Globals.PREY_FOV, ROV=Globals.PREY_ROV)

        self.distances = [0, 0, 0, 0, 0]

    def deepcopy(self):
        newprey = PreyAnimal(self.surface, self.x, self.y)
        newprey.Network = self.Network
        newprey.newgen()
        return newprey

    def recharge(self):
        if self.vel <=0:
            self.Energy += 0.5
    
    # def turningGraph(self, x):
    #     x = (4 * (x - 0.5)**2)**1
    #     return x

    def avoid(self):
        if max(self.distances)> 0:
            # macht alle rays sichtbar, falls der hunter etwas sieht
            self.rayGroup.draw(self.surface)
            
            # führt die forward Funktion im Neuralen Netzwerk aus, sobald die Rays etwas sehen.
            netResult = self.Network.forward(self.distances)
            
            #Änderung des Winkels
            ResultTurn = netResult[0]**2
            if (netResult[0] < 0):
                self.rotate(turn_right=False, turn_angle=ResultTurn)
            elif (netResult[0] > 0):
                self.rotate(turn_right=True, turn_angle=ResultTurn)

            #Änderung der Geschwindigkeit
            ResultSpeed = netResult[1]**2
            if netResult[1] > 0:
                self.increase_speed(ResultSpeed)
            elif netResult[1] < 0:
                self.reduce_speed(ResultSpeed)

    def update(self, hunterGroup):
        if self.Energy >= 0:
            self.recharge()

        self.distances = Animal.update(self, hunterGroup)
        self.avoid()