import pygame
import os

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")

#Color Library
BG_1color = (255, 255, 255)

#Frames Per Second Limiter
FPS = 60

#Picture height & length
ANIMAL_LENGTH = 500
ANIMAL_HEIGHT = (ANIMAL_LENGTH/16)*9

#Assets loading
HUNTER_IMAGE = pygame.image.load(os.path.join('Assets', 'fogs.png'))
HUNTER = pygame.transform.scale(HUNTER_IMAGE, (ANIMAL_LENGTH, ANIMAL_HEIGHT))



def draw_window():
    WIN.fill(BG_1color)
    WIN.blit(HUNTER, (0, 0))
    pygame.display.update()

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        draw_window()

    pygame.quit()

if __name__ == "__main__":
    main()