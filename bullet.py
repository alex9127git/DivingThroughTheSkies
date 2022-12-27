"""Класс спрайта пули."""
import pygame
from rendering import load_image
from math import cos, sin, pi
from const import BULLET_SPEED, WIDTH, HEIGHT


class Bullet(pygame.sprite.Sprite):
    def __init__(self, aircraft, dmg, velocity, *groups):
        super().__init__(*groups)
        self.x, self.y = aircraft.x, aircraft.y
        self.angle = aircraft.angle
        self.orig = pygame.transform.rotate(load_image("bullet.png", colorkey="white"), self.angle)
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
