import pygame

# Diese Funktion nimmt das Image und skaliert die Grösse davon mit dem factor
def scale_image(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)