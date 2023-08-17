import pygame

WIDTH, HEIGHT = 1600, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI Hunters")
def main():

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    main()