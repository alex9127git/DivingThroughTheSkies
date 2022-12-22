import pygame
from bullet import Bullet
from const import WIDTH, HEIGHT, MAX_ACCELERATION, COOLDOWN
from rendering import load_image
from math import asin, degrees


class Aircraft(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.orig = pygame.transform.scale(load_image("aircraft.png", colorkey=-1), (60, 60))
        self.image = self.orig
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.ax = 0
        self.ay = 0
        self.angle = 0
        self.cooldown = COOLDOWN

    def accelerate(self, dx, dy):
        self.ax += dx
        self.ay += dy
        if self.ax >= MAX_ACCELERATION:
            self.ax = MAX_ACCELERATION
        if self.ax <= -MAX_ACCELERATION:
            self.ax = -MAX_ACCELERATION
        if self.ay >= MAX_ACCELERATION:
            self.ay = MAX_ACCELERATION
        if self.ay <= -MAX_ACCELERATION:
            self.ay = -MAX_ACCELERATION

    def update(self, secs, cursor):
        self.cooldown -= secs
        if self.cooldown < 0:
            self.cooldown = 0
        self.x += self.ax * secs
        self.y += self.ay * secs
        self.ax *= 0.99
        self.ay *= 0.99
        if abs(self.ax) <= 1:
            self.ax = 0
        if abs(self.ay) <= 1:
            self.ay = 0
        if self.y < -50:
            self.y = HEIGHT + 50
        elif self.y > HEIGHT + 50:
            self.y = -50
        elif self.x < -50:
            self.x = WIDTH + 50
        elif self.x > WIDTH + 50:
            self.x = -50
        dx = cursor.rect.centerx - self.rect.centerx
        dy = cursor.rect.centery - self.rect.centery
        d = max(((dx ** 2) + (dy ** 2)) ** 0.5, 0.1)
        angle = -degrees(asin(dy / d))
        if dx < 0:
            angle = 180 - angle
        self.angle = angle
        self.image = pygame.transform.rotate(self.orig, angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def shoot(self, bullets, sprites):
        if self.cooldown == 0:
            Bullet(self, bullets, sprites)
            self.cooldown = COOLDOWN
