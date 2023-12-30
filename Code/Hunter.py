import pygame
import random
from Animal import *
from utils import *
from Globals import *
class HunterAnimal(Animal):
    IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), animal_size)
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
        #self.STRTvel = random.randint(1, 3)
        #self.STRTangle = random.randint(0, 360)
        #self.Angle_SPD = random.randint(3, 5)
        self.fitness = 0
        #self.FOVdis = 30
        #self.seen = 0
        self.surface = surface
        self.Energy = hunter_energy
        self.no_hunt = 0
    
        #self.STRTangle = 0
        Animal.__init__(self, "hunter", surface, rays=5, FOV=HUNTER_FOV, ROV=HUNTER_ROV)

        #Distanzenliste für die Rays im Raycasting
        self.distances = [-1, -1, -1, -1, -1]

    def deepcopy(self):
        newhunter = HunterAnimal(self.surface, self.x, self.y)
        newhunter.newgen()
        return newhunter
    
    #def seePrey(self, index, distance):
    #    self.distances[index] = distance

    def turningGraph(self, x):
        x = (4 * (x - 0.5)**2)**1
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
        self.Energy = hunter_energy

    def update(self, preyGroup):
        if self.vel <= 3:
            self.vel = 3

        if self.Energy <= 0:
            pygame.sprite.Sprite.kill(self)
        for index, ray in enumerate(self.rayGroup.sprites()):
            self.distances[index] = -1

        self.distances = Animal.update(self, preyGroup)
        self.hunt()
        if self.no_hunt > 0:
            self.no_hunt -= 1
    