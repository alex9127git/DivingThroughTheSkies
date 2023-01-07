"""Класс спрайта пули."""
import pygame
from rendering import load_image
from math import cos, sin, pi
from const import WIDTH, HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, angle, dmg, velocity, *groups):
        super().__init__(*groups)
        self.x, self.y = start_x, start_y
        self.angle = angle
        filename = "bullet.png" if dmg < 10 else ("bigbullet.png" if dmg < 100 else "hugebullet.png")
        self.orig = pygame.transform.rotate(load_image(filename, colorkey="white"), self.angle)
        self.image = self.orig
        self.rect = pygame.Rect(self.x - 2, self.y - 2, 5, 5)
        self.rect.center = self.x, self.y
        self.v = velocity
        self.dmg = dmg

    def update(self, secs):
        self.x += self.v * cos(self.angle * pi / 180) * secs
        self.y -= self.v * sin(self.angle * pi / 180) * secs
        self.rect.center = self.x, self.y
        if not (0 <= self.x <= WIDTH and 0 <= self.y <= HEIGHT):
            self.kill()

    def kill(self):
        super().kill()
        del self
