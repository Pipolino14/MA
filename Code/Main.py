import pygame
import time
import math
import uuid
import random
from utils import *
from Animal import *
from Environment import *
from Hunter import *
from Prey import *

#Assets loading


BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)
COLLIDER_IMG = scale_image(pygame.image.load("Code/Assets/collideTEST.PNG"), 1)
COLLIDER_TEST_MASK = pygame.mask.from_surface(COLLIDER_IMG)

#Window dimensions 
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")



#Frames Per Second Limiter
FPS = 60
VEL = 5

GameHunter = pygame.sprite.Group()
GamePrey = pygame.sprite.Group()
#EatingHunters = pygame.sprite.Group()


def Draw(win, images):
    for img, pos in images:
        win.blit(img, pos)
    
#    Hanimals = HunterAnimalsDictionary.values()
#    Panimals = PreyAnimalsDictionary.values()
    
#    for hunter in Hanimals:
#        hunter.draw(win)
#    for prey in Panimals:
#        prey.draw(win)
    pygame.display.update()

def check_collide():
    spriteGroup = pygame.sprite.groupcollide(GameHunter, GamePrey, False, True, pygame.sprite.collide_mask)
    for x in spriteGroup.keys():
        x.recharge()
        print("Recharged")
    #print(EatingList[0])
    #Here is where we stopped.
    #We want to recharge the Energy of the Hunter who has eaten a animal.
    #Solution 1: extract Hunter from List and "feed" it
    

def collided(H, P):
    print(H, P)

run = True
clock = pygame.time.Clock()
images = [(BG_IMG, (0, 0)), (COLLIDER_IMG, (0,0))]
imgRect = pygame.Rect(0,0,WIDTH,HEIGHT)
MyEnvironment = Environment()

walker = HunterAnimal()





cords = 0

#MyEnvironment.Hanimals, MyEnvironment.Panimals
while run:
    clock.tick(FPS)
    WIN.blit(BG_IMG,(0, 0)) 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    moved = False
    
    if keys[pygame.K_1]:
        walker.x = 300
        GameHunter.add(walker)
    if keys[pygame.K_2]:
        GamePrey.add(PreyAnimal())
    if keys[pygame.K_3]:
        GameHunter.add(HunterAnimal())
        
    if keys[pygame.K_a]:
        walker.rotate(left=True)
    if keys[pygame.K_d]:
        walker.rotate(right=True)
    if keys[pygame.K_w]:
        walker.increase_speed(0.3)
    if keys[pygame.K_s]:
        walker.reduce_speed(0.3)

    
    #off window bounce prototype
    #collision checker for the walker
    if walker.collision(COLLIDER_TEST_MASK):
        h = 1
    
    #collision checker for the walker
    #print(pygame.sprite.Group.sprites(GameHunter))
    
    
    #pygame.display.update([imgRect])
    GamePrey.update()
    GamePrey.draw(WIN)
    GameHunter.update()
    GameHunter.draw(WIN)
    pygame.display.flip()
    check_collide()


    

    
    #pygame.display.update()



pygame.quit()
