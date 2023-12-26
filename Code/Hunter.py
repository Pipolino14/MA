import pygame
import random
import copy
from Animal import *
from utils import *

class HunterAnimal(Animal):
    IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), 0.35)
    IMGHEI = IMG.get_height()
    IMGWID = IMG.get_height()
    MASK = pygame.mask.from_surface(IMG)
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
        self.STRTvel = random.randint(1, 3)
        self.STRTangle = random.randint(0, 360)
        self.Angle_SPD = random.randint(3, 5)
        self.fitness = 0
        #self.FOVdis = 30
        self.seen = 0
        self.surface = surface
        self.Energy = 600

    
        #self.STRTangle = 0
        Animal.__init__(self, "hunter", surface, rays=5, FOV=50, ROV=500)

        #Distanzenliste für die Rays im Raycasting
        self.distances = [-1, -1, -1, -1, -1]

    def deepcopy(self):
        newhunter = HunterAnimal(self.surface, self.x, self.y)
        newhunter.newgen()
        return newhunter
    
    #def seePrey(self, index, distance):
    #    self.distances[index] = distance

    def turningGraph(self, x):
        x = (4 * (x - 0.5)**2)**2
        return x
    
    def hunt(self):
        if(True): #max(self.distances)> -1
            #print(self.distances)
            # macht alle rays sichtbar, falls der hunter etwas sieht
            #print(np.around(self.distances, 1))
            self.rayGroup.draw(self.surface)

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




            # if self.Network.forward(self.distances)[0] < 0.33:
            #     self.rotate(left=True)
            # elif self.Network.forward(self.distances)[0] > 0.66:
            #     self.rotate(right=True)
            # if self.Network.forward(self.distances)[1] > 0.66:
            #     self.increase_speed(0.1)
            # elif self.Network.forward(self.distances)[1] < 0.33:
            #     self.reduce_speed(0.1)
    


    def recharge(self):
        #self.Energy = self.Energy + 600
        self.Energy = 600

    def update(self, preyGroup):
        if self.vel <= 3:
            self.vel = 3

        

        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)
        for index, ray in enumerate(self.rayGroup.sprites()):
            self.distances[index] = -1
        #for (index, ray) in enumerate(self.rayGroup.sprites()):
        #    ray.checkSeeAnimal(index, (self.x, self.y), preyGroup, self.seePrey)
        self.distances = Animal.update(self, preyGroup)
        self.hunt()
    
    