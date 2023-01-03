"""Класс спрайта истребителя."""
import pygame
from random import randint, randrange
from bullet import Bullet
from const import WIDTH, HEIGHT, BULLET_SPEED
from enemy import Enemy
from math import asin, degrees


class Fighter(Enemy):
    def __init__(self, difficulty, aircraft, *groups):
        super().__init__("fighter", difficulty, *groups)
        side = randrange(4)  # 0 для верхнего края, 1 для нижнего, 2 для левого, 3 для правого
        # генерация начальных координат
        self.x, self.y = ((randint(50, WIDTH - 50), 0), (randint(50, WIDTH - 50), HEIGHT),
                          (0, randint(50, HEIGHT - 50)), (WIDTH, randint(50, HEIGHT - 50)))[side]
        # генерация конечных координат
        self.goal_x, self.goal_y = aircraft.x, aircraft.y
        reach_time = max((9 / (self.difficulty - 0.4)) ** 0.5, 1)
        # вычисление скорости и ускорения
        sx = self.goal_x - self.x
        sy = self.goal_y - self.y
        self.vx = 2 * sx / reach_time
        self.vy = 2 * sy / reach_time
        self.ax = self.vx / reach_time
        self.ay = self.vy / reach_time
        self.direction_x = 1 if self.vx > 0 else -1
        self.direction_y = 1 if self.vy > 0 else -1
        # вычисление угла
        d = max(((self.vx ** 2) + (self.vy ** 2)) ** 0.5, 0.1)
        angle = -degrees(asin(self.vy / d))
        if self.vx < 0:
            angle = 180 - angle
        self.angle = angle
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.hp = int(3 * round(self.difficulty, 1))
        self.dmg = 1
        self.bullet_dmg = 1
        self.stop_timer = 1 / round(self.difficulty, 1)
        self.timer = 0
        self.experience_dropped = randint(int(2 * self.difficulty), int(7 * self.difficulty))

    def update(self, secs):
        if self.timer:
            self.timer -= secs
            if self.timer < 0:
                self.timer = 0
        else:
            self.x += self.vx * secs
            self.y += self.vy * secs
            self.vx -= self.ax * secs
            self.vy -= self.ay * secs
            self.rect.center = self.x, self.y

    def update_strategy(self, aircraft, groups):
        if self.vx // self.direction_x < 0 or self.vy // self.direction_y < 0:
            # вычисление новых координат, скорости и ускорения
            reach_time = max((9 / (self.difficulty - 0.4)) ** 0.5, 1)
            self.goal_x, self.goal_y = aircraft.x, aircraft.y
            sx = self.goal_x - self.x
            sy = self.goal_y - self.y
            self.vx = 2 * sx / reach_time
            self.vy = 2 * sy / reach_time
            self.ax = self.vx / reach_time
            self.ay = self.vy / reach_time
            self.direction_x = 1 if self.ax > 0 else -1
            self.direction_y = 1 if self.ay > 0 else -1
            # вычисление угла
            d = max(((self.vx ** 2) + (self.vy ** 2)) ** 0.5, 0.1)
            angle = -degrees(asin(self.vy / d))
            if self.vx < 0:
                angle = 180 - angle
            self.angle = angle
            self.image = pygame.transform.rotate(self.orig, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = self.x, self.y
            Bullet(self.x, self.y, self.angle, self.bullet_dmg, BULLET_SPEED / 2, groups["enemy_bullets"],
                   groups["sprites"])
            self.timer = self.stop_timer
