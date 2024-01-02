#import pygame
#import random
from Animal import *
from utils import *
from Globals import *
class HunterAnimal(Animal):
    def __init__(self, surface, posX = None,posY = None):
        self.fitness = 0
        self.Energy = Globals.hunter_energy
        self.no_hunt = 0

        Animal.__init__(self, "hunter", surface, posX, posY, rays=5,
                        FOV=Globals.HUNTER_FOV, ROV=Globals.HUNTER_ROV)

        self.distances = [0, 0, 0, 0, 0]

    def deepcopy(self):
        newhunter = HunterAnimal(self.surface, self.x, self.y)
        newhunter.Network = self.Network
        newhunter.newgen()
        return newhunter
    
    def hunt(self):
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

    def recharge(self):
        self.Energy = Globals.hunter_energy

    def update(self, preyGroup):
        if self.vel <= 3:
            self.vel = 3

        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)

        self.distances = Animal.update(self, preyGroup)
        self.hunt()
        if self.no_hunt > 0:
            self.no_hunt -= 1
    