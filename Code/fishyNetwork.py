import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
FOV = math.radians(360)
BACKGROUND_COLOR = (50, 50, 50)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Raycasting Demo with Blocking Rect")
clock = pygame.time.Clock()

# Blocker rectangle
blocker_rect = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 2)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Get mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    for angle in range(0, 360, 5):
        # Calculate ray direction
        ray_dir_x = math.cos(math.radians(angle))
        ray_dir_y = math.sin(math.radians(angle))

        # Normalize the ray direction
        ray_length = math.sqrt(ray_dir_x**2 + ray_dir_y**2)
        ray_dir_x /= ray_length
        ray_dir_y /= ray_length

        # Cast the ray
        ray_length = 500
        end_x = int(mouse_x + ray_length * ray_dir_x)
        end_y = int(mouse_y + ray_length * ray_dir_y)

        # Check for intersection with the blocker rectangle
        if blocker_rect.collidepoint(end_x, end_y):
            pygame.draw.line(screen, RED, (mouse_x, mouse_y), (end_x, end_y), 2)
            pygame.draw.rect(screen, RED, blocker_rect, 2)
            break
        else:
            pygame.draw.line(screen, WHITE, (mouse_x, mouse_y), (end_x, end_y), 2)

    pygame.display.flip()
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
sys.exit()
