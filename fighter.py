"""Класс спрайта истребителя."""
import pygame
from random import randint, randrange
from bullet import Bullet
from const import WIDTH, HEIGHT, BULLET_SPEED, shoot_sfx
from enemy import Enemy
from math import asin, degrees


class Fighter(Enemy):
    def __init__(self, difficulty, aircraft, *groups):
        super().__init__("fighter", difficulty, *groups)
        self.orig = pygame.transform.scale(self.orig, (50, 50))
        side = randrange(4)  # 0 для верхнего края, 1 для нижнего, 2 для левого, 3 для правого
        # генерация начальных координат
        self.x, self.y = ((randint(50, WIDTH - 50), 0), (randint(50, WIDTH - 50), HEIGHT),
                          (0, randint(50, HEIGHT - 50)), (WIDTH, randint(50, HEIGHT - 50)))[side]
        self.goal_x = self.goal_y = self.vx = self.vy = self.ax = self.ay = self.direction_x = self.direction_y = 0
        self.rotate_to_aircraft(aircraft)
        self.hp = int(3 * round(self.difficulty ** (1 + (self.difficulty - 1) / 4), 1))
        self.max_hp = self.hp
        self.dmg = 1
        self.bullet_dmg = 1
        self.stop_timer = max(1.5 / round(self.difficulty ** 0.5, 1), 0.5)
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
        if (self.vx // self.direction_x < 0 or self.vy // self.direction_y < 0) and self.timer == 0:
            shoot_sfx.play()
            self.rotate_to_aircraft(aircraft)
            Bullet(self.x, self.y, self.angle, self.bullet_dmg, BULLET_SPEED, groups["enemy_bullets"],
                   groups["sprites"])
            self.timer = self.stop_timer
        if self.timer > 0:
            self.rotate_to_aircraft(aircraft)

    def rotate_to_aircraft(self, aircraft):
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
