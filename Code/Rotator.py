import pygame
import math
from utils import *

class  Rotator():
    
    hunter_rays = []
    hunter_masks = []
    prey_rays = []
    prey_masks = []

    def create_rays(surface, hunter_view_range, prey_view_range):
        hunter_rect_size = 2 * hunter_view_range
        Rotator.hunter_image = pygame.Surface([hunter_rect_size, hunter_rect_size])
        Rotator.hunter_image.set_colorkey((255,0,0))
        prey_rect_size = 2 * prey_view_range
        Rotator.prey_image = pygame.Surface([prey_rect_size, prey_rect_size])
        Rotator.prey_image.set_colorkey((255,0,0))

        for angle in range(0, 360):
            rad_angle = math.radians(angle)
            hunter_x = math.sin(rad_angle) * hunter_view_range
            hunter_y = math.cos(rad_angle) * hunter_view_range
            prey_x = math.sin(rad_angle) * prey_view_range
            prey_y = math.cos(rad_angle) * prey_view_range

            hunter_ray = pygame.draw.line(
                Rotator.hunter_image,
                (0, 0, 255),
                (hunter_view_range, hunter_view_range),
                (hunter_view_range - hunter_x, hunter_view_range - hunter_y),
                1,
            )
            hunter_mask = pygame.mask.from_surface(Rotator.hunter_image)
            Rotator.hunter_rays.append(hunter_ray)
            Rotator.hunter_masks.append(hunter_mask)

            prey_ray = pygame.draw.line(
                Rotator.prey_image,
                (0, 0, 255),
                (prey_view_range, prey_view_range),
                (prey_view_range - prey_x, prey_view_range - prey_y),
                1,
            )
            prey_mask = pygame.mask.from_surface(Rotator.prey_image)
            Rotator.prey_rays.append(prey_ray)
            Rotator.prey_masks.append(prey_mask)

    def get_image(animal):
        image = None
        if (animal == "hunter"):
            image = Rotator.hunter_image
        elif (animal == "prey"):
            image = Rotator.prey_image
        return image

    def get_mask(animal, deg_angle) -> pygame.Mask:
        index = int(deg_angle) % 360
        if (index < 0):
            index = 359 + index
        if (index == 360):
            index = 0
        mask = None
        if (animal == "hunter"):
            mask = Rotator.hunter_masks[index]
        elif (animal == "prey"):
            mask = Rotator.prey_masks[index]
        return mask