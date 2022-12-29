"""Класс спрайта самолета."""
import pygame
from bullet import Bullet
from const import WIDTH, HEIGHT, MAX_ACCELERATION, COOLDOWN, BULLET_SPEED, AIRCRAFT_HP, calculate_aircraft_experience
from experience import Experience
from explosion import Explosion
from rendering import load_image
from math import asin, degrees


class Aircraft(pygame.sprite.Sprite):
    class UpgradesRecord:
        def __init__(self):
            self.upgrade_branch = -1
            self.upgrades = [0, 0, 0]

        def __getitem__(self, item):
            return self.upgrades[item]

        def __iadd__(self, other):
            if isinstance(other, int) and 0 <= other <= 2:
                self.upgrades[other] += 1
            return self

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
        self.max_hp = AIRCRAFT_HP
        self.hp = self.max_hp
        self.level = 0
        self.experience = 0
        self.experience_to_next_level = calculate_aircraft_experience(self.level)
        self.bullet_dmg = 1
        self.upgrades = Aircraft.UpgradesRecord()

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
        if self.hp <= 0:
            self.kill()

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
        bullet = pygame.sprite.spritecollideany(self, groups["enemy_bullets"],
                                                collided=pygame.sprite.collide_rect_ratio(.5))
        if bullet is not None and isinstance(bullet, Bullet):
            self.hp -= bullet.dmg
            Explosion(self.x, self.y, groups["sprites"], groups["explosions"])
            bullet.kill()

    def check_experience(self, groups):
        xp = pygame.sprite.spritecollideany(self, groups["experience_coins"])
        if xp is not None and isinstance(xp, Experience):
            self.experience += xp.xp
            xp.kill()
        if self.experience >= self.experience_to_next_level and self.level <= 9:
            self.experience -= self.experience_to_next_level
            self.level += 1
            self.experience_to_next_level = calculate_aircraft_experience(self.level)
            return self.level
        return -1

    def has_branch(self):
        return self.upgrades.upgrade_branch != -1

    def assign_branch(self, branch):
        self.upgrades.upgrade_branch = branch
