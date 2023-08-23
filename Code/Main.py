import pygame
import os

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")

#Color Library
BG_1color = (255, 255, 255)

#Frames Per Second Limiter
FPS = 60
VEL = 5

#Picture height & length
ANIMAL_LENGTH = 500
ANIMAL_HEIGHT = (ANIMAL_LENGTH/16)*9

#Assets loading
HUNTER_IMAGE = pygame.image.load(os.path.join('Assets', 'fogs.png'))
HUNTER_IMAGE_RESIZED = pygame.transform.scale(HUNTER_IMAGE, (ANIMAL_LENGTH, ANIMAL_HEIGHT))



def draw_window(hunter):
    WIN.fill(BG_1color)
    WIN.blit(HUNTER_IMAGE_RESIZED, (hunter.x, hunter.y))
    pygame.display.update()

def main():
    #drawing rectangles for movement of pictures
    hunter = pygame.Rect(100, 300, ANIMAL_LENGTH, ANIMAL_HEIGHT) 

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        #WASD-Key movement (Have to figure out a way to make it an FOV and turn it with WASD)
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_d]:
            hunter.x += VEL
        
        draw_window(hunter)

    pygame.quit()

if __name__ == "__main__":
    main()