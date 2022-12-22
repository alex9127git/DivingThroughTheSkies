import pygame
from rendering import load_image


class Cursor(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image("cursor.png", colorkey=-1), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = 0, 0

    def update_pos(self, x, y):
        self.rect.center = x, y
