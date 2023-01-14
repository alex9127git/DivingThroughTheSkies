"""Класс, управляющий механикой тумана."""
from random import randrange, randint

import pygame

import rendering
from const import WIDTH, HEIGHT


class FogManager(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.enabled = False
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()
        self.timer = 10
        self.x = self.y = self.vx = self.vy = 0

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.timer = 10
        self.image = pygame.Surface((1, 1))
        self.rect = self.image.get_rect()

    def reposition(self):
        scale = randint(400, 700)
        self.image = pygame.transform.scale(rendering.load_image(f"fog{randint(1, 3)}.png"),
                                            (scale, scale))
        self.rect = self.image.get_rect()
        side = randrange(4)
        self.x, self.y = ((randint(50, WIDTH - 50), -scale // 2), (randint(50, WIDTH - 50), HEIGHT + scale // 2),
                          (-scale // 2, randint(50, HEIGHT - 50)), (WIDTH + scale // 2, randint(50, HEIGHT - 50)))[side]
        self.vy = randint(2, 4) * (-1 if side == 1 else 1) if side < 2 else 0
        self.vx = randint(2, 4) * (-1 if side == 3 else 1) if side >= 2 else 0

    def update(self, secs):
        if self.enabled:
            if self.timer == 0:
                self.x += self.vx
                self.y += self.vy
                if self.y < -500:
                    self.timer = 3
                if self.y > HEIGHT + 500:
                    self.timer = 3
                if self.x < -500:
                    self.timer = 3
                if self.x > WIDTH + 500:
                    self.timer = 3
            else:
                self.image = pygame.Surface((1, 1))
                self.rect = self.image.get_rect()
                self.timer -= secs
                if self.timer < 0:
                    self.timer = 0
                    self.reposition()
            self.rect.center = self.x, self.y
