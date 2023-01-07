"""Класс спрайта дрона."""
import pygame
from bullet import Bullet
from const import BULLET_SPEED
from enemy import Enemy
from math import asin, degrees


class Cannon(Enemy):
    def __init__(self, mounted, dx, dy, difficulty, cannon_type, hp, *groups):
        super().__init__(cannon_type, difficulty, *groups)
        self.mounted = mounted
        self.dx, self.dy = dx, dy
        self.x, self.y = self.mounted.x + dx, self.mounted.y + dy
        self.angle = 270
        self.orig = pygame.transform.scale(self.orig, (50, 50))
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.hp = hp
        self.max_hp = self.hp
        self.dmg = 1
        self.experience_dropped = 0
        self.cannon_type = cannon_type

    def update(self, secs):
        self.x, self.y = self.mounted.x + self.dx, self.mounted.y + self.dy
        self.image = pygame.transform.rotate(self.orig, self.angle)
        pygame.draw.rect(self.image, "white",
                         (self.image.get_width() // 2 - self.orig.get_width() // 2, self.image.get_height() // 2 + 20,
                          self.orig.get_width(), 5), 0)
        pygame.draw.rect(self.image, "red",
                         (self.image.get_width() // 2 - self.orig.get_width() // 2, self.image.get_height() // 2 + 20,
                          self.orig.get_width() / self.max_hp * self.hp, 5), 0)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def track(self, aircraft):
        dx = aircraft.rect.centerx - self.rect.centerx
        dy = aircraft.rect.centery - self.rect.centery
        d = max(((dx ** 2) + (dy ** 2)) ** 0.5, 0.1)
        angle = -degrees(asin(dy / d))
        if dx < 0:
            angle = 180 - angle
        self.angle = angle

    def shoot(self, groups):
        if self.cannon_type == "cannon":
            Bullet(self.x, self.y, self.angle, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
        elif self.cannon_type == "radial cannon":
            Bullet(self.x, self.y, self.angle, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
            Bullet(self.x, self.y, self.angle + 60, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
            Bullet(self.x, self.y, self.angle + 120, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
            Bullet(self.x, self.y, self.angle + 180, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
            Bullet(self.x, self.y, self.angle + 240, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
            Bullet(self.x, self.y, self.angle + 300, self.dmg,
                   BULLET_SPEED / 4, groups["enemy_bullets"], groups["sprites"])
