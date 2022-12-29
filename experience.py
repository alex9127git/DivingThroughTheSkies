"""Класс спрайта монет опыта."""
from random import randint

import pygame

from rendering import load_image


class Experience(pygame.sprite.Sprite):
    def __init__(self, x, y, xp_value, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(load_image(f"{xp_value}xp.png", colorkey=-1), (20, 20))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.ax = randint(-50, 50)
        self.ay = randint(-50, 50)
        self.rect.center = self.x, self.y
        self.xp = xp_value

    def update(self, secs):
        self.x += self.ax * secs
        self.y += self.ay * secs
        self.ax *= 0.99
        self.ay *= 0.99
        if abs(self.ax) <= 1:
            self.ax = 0
        if abs(self.ay) <= 1:
            self.ay = 0
        self.rect.center = self.x, self.y

    def kill(self):
        super().kill()
        del self
