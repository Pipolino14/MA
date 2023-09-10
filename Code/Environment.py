import pygame
import uuid
import random
from Hunter import *
from Prey import *

class Environment:
    Hanimals = {}
    Panimals = {}


    def AddHunter(self):
        id = str(uuid.uuid4())
        print(id)
        hunterAnimal = HunterAnimal(4,4, id)
        hunterAnimal.x = random.randint(100, 1600)
        hunterAnimal.y = random.randint(100, 900)
        self.Hanimals.update({id:hunterAnimal})
    
    def AddPrey(self):
        id = str(uuid.uuid4())
        print(id)
        preyAnimal = PreyAnimal(4,4,id)
        preyAnimal.x = random.randint(100, 1600)
        preyAnimal.y = random.randint(100, 900)
        self.Panimals.update({id:preyAnimal})
