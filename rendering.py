import os
import sys
import pygame
from const import WIDTH, HEIGHT


def initialize():
    pygame.init()
    size = WIDTH, HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill("white")
    pygame.display.set_caption("Diving Through The Skies")
    return screen


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден", file=sys.stderr)
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
