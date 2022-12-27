"""Класс спрайта самолета."""
import pygame
from bullet import Bullet
from const import WIDTH, HEIGHT, MAX_ACCELERATION, COOLDOWN, BULLET_SPEED
from explosion import Explosion
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
        self.hp = 3
        self.bullet_dmg = 1

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

    def update(self, secs):
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

    def rotate_to_cursor(self, cursor):
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

    def shoot(self, groups):
        if self.cooldown == 0:
            Bullet(self, self.bullet_dmg, BULLET_SPEED, groups["player_bullets"], groups["sprites"])
            self.cooldown = COOLDOWN

    def check_bullet_collisions(self, groups):
        """Проверяет столкновение с пулями."""
        bullet = pygame.sprite.spritecollideany(self, groups["enemy_bullets"])
        if bullet is not None and isinstance(bullet, Bullet):
            self.hp -= bullet.dmg
            Explosion(self.x, self.y, groups["sprites"], groups["explosions"])
            bullet.kill()
            if self.hp <= 0:
                self.kill()
