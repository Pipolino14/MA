import pygame
import time
import math
import uuid
import random
from utils import scale_image, blit_rotate_center

#Assets loading
HUNTER_IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), 1)
PREY_IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), 1)
BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)
COLLIDER_IMG = scale_image(pygame.image.load("Code/Assets/collideTEST.PNG"), 1)
COLLIDER_TEST_MASK = pygame.mask.from_surface(COLLIDER_IMG)

#masks for Hunter and prey for collision
HUNTER_MASK = pygame.mask.from_surface(HUNTER_IMG)
PREY_MASK = pygame.mask.from_surface(PREY_IMG)

#Window dimensions 
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")



#Frames Per Second Limiter
FPS = 60
VEL = 5

class Animal:
    def __init__(self, max_vel, rotation_vel, id):
        self.img = self.IMG
        self.mask = self.MASK
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1
        self.id = id

    
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel
    
    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()


    def move(self):
        #converting the current facing angle to RAD
        radians = math.radians(self.angle)
        #cos(RichtungsWinkel) * Hypothenuse{velocity vector} = Gegenkatethe --> Y movement
        vertical = math.cos(radians) * self.vel
        #sin(RichtungsWinkel) * Hypothenuse{velocity vector} = Ankatethe --> X movement
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal
    
    def reduce_speed(self):
        self.vel = max(self.vel - self.acceleration / 2, 0)
        self.move()


    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), (self.angle+90))

    def collision(self, mask, x=0, y=0):
        animal_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        touch = mask.overlap(animal_mask, offset)
        return touch
    
    def bounce(self):
        self.vel = -self.vel


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



class HunterAnimal(Animal):
    IMG = HUNTER_IMG
    MASK = HUNTER_MASK
    START_POS = (300, 300)

class PreyAnimal(Animal):
    IMG = PREY_IMG
    START_POS = (500, 500)


def draw(win, images, HunterAnimalsDictionary):
    for img, pos in images:
        win.blit(img, pos)
    
    Hanimals = HunterAnimalsDictionary.values()

    #Hanimals[0].draw(win)

    for hunter in Hanimals:
        hunter.draw(win)
    #prey_animal.draw(win)
    pygame.display.update()



run = True
clock = pygame.time.Clock()
images = [(BG_IMG, (0, 0)), (COLLIDER_IMG, (0,0))]
MyEnvironment = Environment()

#
#print(walker)
MyEnvironment.AddHunter()
MyEnvironment.AddHunter()
MyEnvironment.AddHunter()
MyEnvironment.AddHunter()

walker = list(Environment.Hanimals.values())[0]

cords = 0
#hunter_animal = HunterAnimal(4, 4)
#hunter_animal2 = HunterAnimal(4, 4)
#prey_animal = PreyAnimal(4, 4)

while run:
    clock.tick(FPS)
    draw(WIN, images, MyEnvironment.Hanimals)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_a]:
        walker.rotate(left=True)
    if keys[pygame.K_d]:
        walker.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        walker.move_forward()    
    if not moved:
        walker.reduce_speed()

    
    #off window bounce prototype
    if walker.x < 0:
        walker.bounce()
        print("Owie, the wall")
    if walker.y < 0:
        walker.bounce()
        print("Owie, the ceiling")
    if walker.x > WIDTH - HUNTER_IMG.get_width():
        walker.bounce()
        print("Owie, the other wall")
    if walker.y > HEIGHT - HUNTER_IMG.get_width():
        walker.bounce()
        print("Owie, the floor")

    #collision checker for the walker
    if walker.collision(COLLIDER_TEST_MASK):
        print(cords)
        cords = cords + 1
    

    
    


    


pygame.quit()
