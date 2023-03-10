"""Класс спрайта дрона."""
import pygame
from random import randint, randrange
from const import WIDTH, HEIGHT
from enemy import Enemy
from math import asin, degrees


class Drone(Enemy):
    def __init__(self, difficulty, *groups):
        super().__init__("drone", difficulty, *groups)
        side = randrange(4)  # 0 для верхнего края, 1 для нижнего, 2 для левого, 3 для правого
        # генерация начальных координат
        self.x, self.y = ((randint(50, WIDTH - 50), 0), (randint(50, WIDTH - 50), HEIGHT),
                          (0, randint(50, HEIGHT - 50)), (WIDTH, randint(50, HEIGHT - 50)))[side]
        # вычисление скорости
        self.vy = randint(150, 250) * (-1 if side == 1 else 1) if side < 2 else randint(-50, 50)
        self.vx = randint(150, 250) * (-1 if side == 3 else 1) if side >= 2 else randint(-50, 50)
        # вычисление угла
        d = max(((self.vx ** 2) + (self.vy ** 2)) ** 0.5, 0.1)
        angle = -degrees(asin(self.vy / d))
        if self.vx < 0:
            angle = 180 - angle
        self.angle = angle
        self.orig = pygame.transform.scale(self.orig, (50, 50))
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.hp = int(self.difficulty ** (1 + (self.difficulty - 1) / 4))
        self.max_hp = self.hp
        self.dmg = 1
        self.experience_dropped = randint(int(1 * self.difficulty), int(3 * self.difficulty))

    def update(self, secs):
        self.x += self.vx * secs
        self.y += self.vy * secs
        self.rect.center = self.x, self.y
        if self.y < -50:
            self.y = HEIGHT + 50
        elif self.y > HEIGHT + 50:
            self.y = -50
        elif self.x < -50:
            self.x = WIDTH + 50
        elif self.x > WIDTH + 50:
            self.x = -50
