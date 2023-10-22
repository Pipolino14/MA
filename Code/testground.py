import pygame
from Animal import *
from Hunter import *
from Prey import *


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
VEL = 5

# Load Images
BG_IMG = pygame.image.load("Code/Assets/grass.jpg")
COLLIDER_IMG = pygame.image.load("Code/Assets/collideTEST.PNG")
COLLIDER_TEST_MASK = pygame.mask.from_surface(COLLIDER_IMG)

# Create the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")

# Initialize Groups
GameHunter = pygame.sprite.Group()
GamePrey = pygame.sprite.Group()

# Initialize clock
clock = pygame.time.Clock()

# Preload images
images = [(BG_IMG, (0, 0)), (COLLIDER_IMG, (0, 0))]

# Create a hunter
walker = HunterAnimal(WIN)

run = True

while run:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    keys = pygame.key.get_pressed()

    if keys[pygame.K_1]:
        walker.x = 300
        GameHunter.add(walker)
    if keys[pygame.K_2]:
        GamePrey.add(PreyAnimal(WIN))
    if keys[pygame.K_3]:
        GameHunter.add(HunterAnimal(WIN))
    if keys[pygame.K_a]:
        walker.rotate(left=True)
    if keys[pygame.K_d]:
        walker.rotate(right=True)
    if keys[pygame.K_w]:
        walker.increase_speed(0.3)
    if keys[pygame.K_s]:
        walker.reduce_speed(0.3)

    # Off-window bounce prototype
    if walker.collision(COLLIDER_TEST_MASK):
        h = 1

    # Update and draw the prey
    GamePrey.update()
    GamePrey.draw(WIN)

    # Update and draw the hunters
    GameHunter.update()
    GameHunter.draw(WIN)

    pygame.display.flip()

pygame.quit()
