import pygame
import math

pygame.init()

width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

class MovingObject(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = 0
        self.speed = 2

    def update(self):
        self.angle += self.speed
        self.rect.centerx = width // 2 + 100 * math.cos(math.radians(self.angle))
        self.rect.centery = height // 2 + 100 * math.sin(math.radians(self.angle))

def raycast(origin, target_pos):
    dx = target_pos[0] - origin.rect.centerx
    dy = target_pos[1] - origin.rect.centery

    distance = math.hypot(dx, dy)
    if distance > 0:
        dx, dy = dx / distance, dy / distance

    test_pos = origin.rect.center
    for _ in range(int(distance)):
        test_pos = (test_pos[0] + dx, test_pos[1] + dy)
        if origin.rect.collidepoint(test_pos):
            return test_pos

    return None

obj1 = MovingObject(100, 100, RED)

running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    obj1.update()

    mouse_pos = pygame.mouse.get_pos()

    collision_point = raycast(obj1, mouse_pos)
    if collision_point:
        pygame.draw.line(screen, BLUE, obj1.rect.center, collision_point, 1)

    screen.blit(obj1.image, obj1.rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
