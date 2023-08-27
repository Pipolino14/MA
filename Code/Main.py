import pygame
import time
import math
from utils import scale_image, blit_rotate_center

#Assets loading
HUNTER_IMG = scale_image(pygame.image.load("Code/Assets/hunter.png"), 0.5)
PREY_IMG = scale_image(pygame.image.load("Code/Assets/prey.png"), 0.3)
BG_IMG = scale_image(pygame.image.load("Code/Assets/grass.jpg"), 1)


#Window dimensions 
WIDTH, HEIGHT = BG_IMG.get_width(), BG_IMG.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")

#Color Library
BG_1color = (255, 255, 255)

#Frames Per Second Limiter
FPS = 60
VEL = 5

class Animal:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

    
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

class HunterAnimal(Animal):
    IMG = HUNTER_IMG
    START_POS = (180,200)


def draw(win, images, hunter_animal):
    for img, pos in images:
        win.blit(img, pos)
    
    hunter_animal.draw(win)
    pygame.display.update()



run = True
clock = pygame.time.Clock()
images = [(BG_IMG, (0, 0))]
hunter_animal = HunterAnimal(4, 4)

while run:
    clock.tick(FPS)
    draw(WIN, images, hunter_animal)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        hunter_animal.rotate(left=True)
    if keys[pygame.K_d]:
        hunter_animal.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        hunter_animal.move_forward()
    
    if not moved:
        hunter_animal.reduce_speed()
    

pygame.quit()
