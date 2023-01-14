"""Класс спрайта самолета."""
import pygame
from bullet import Bullet
from const import WIDTH, HEIGHT, MAX_ACCELERATION, BULLET_SPEED, calculate_aircraft_experience, \
    DOUBLE_CANNON_BRANCH, MINIGUN_CANNON_BRANCH, HEAVY_CANNON_BRANCH, calculate_aircraft_hp, shoot_sfx, coin_sfx, \
    heart_sfx, explode_sfx
from experience import Experience
from explosion import Explosion
from health_refill import HealthRefill
from rendering import load_image
from math import asin, degrees, cos, sin

from scrap import Scrap


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

        def calculate_base_dmg(self):
            if self.upgrade_branch == DOUBLE_CANNON_BRANCH:
                dmg = 1
                dmg += sum((2, 2, 4, 4, 7)[:self[1]])
            elif self.upgrade_branch == MINIGUN_CANNON_BRANCH:
                dmg = 1
                dmg += sum((1, 1, 3, 3, 5)[:self[1]])
            elif self.upgrade_branch == HEAVY_CANNON_BRANCH:
                dmg = 3
                dmg += sum((3, 3, 5, 5)[:self[1]])
                dmg += sum((6, 6, 10, 10)[:self[2]])
                dmg *= 1.5 if self[1] == 5 else 1
                dmg *= 2 if self[2] == 5 else 1
            else:
                dmg = 1
            return dmg

        def calculate_cooldown(self):
            if self.upgrade_branch == DOUBLE_CANNON_BRANCH:
                cd = 1
                cd *= 0.9 if self[2] >= 1 else 1
                cd *= 0.9 if self[2] >= 2 else 1
                cd *= 0.8 if self[2] >= 3 else 1
                cd *= 0.8 if self[2] >= 4 else 1
                cd *= 0.6 if self[2] >= 5 else 1
            elif self.upgrade_branch == MINIGUN_CANNON_BRANCH:
                cd = 0.33
                cd *= 0.8 if self[2] >= 1 else 1
                cd *= 0.8 if self[2] >= 2 else 1
                cd *= 0.7 if self[2] >= 3 else 1
                cd *= 0.7 if self[2] >= 4 else 1
                cd *= 0.5 if self[2] >= 5 else 1
            elif self.upgrade_branch == HEAVY_CANNON_BRANCH:
                cd = 1.5
                cd *= 1.2 if self[2] >= 1 else 1
                cd *= 1.2 if self[2] >= 2 else 1
                cd *= 1.2 if self[2] >= 3 else 1
                cd *= 1.2 if self[2] >= 4 else 1
                cd *= 1.5 if self[2] >= 5 else 1
            else:
                cd = 1
            return cd

    def __init__(self, *groups):
        super().__init__(*groups)
        self.orig = pygame.transform.scale(load_image("aircraft.png", colorkey=-1), (60, 60))
        self.image = self.orig
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.wind_x, self.wind_y = 0, 0
        self.ax = 0
        self.ay = 0
        self.angle = 0
        self.cooldown = 1
        self.max_hp = calculate_aircraft_hp()
        self.hp = self.max_hp
        self.level = 0
        self.experience = 0
        self.experience_to_next_level = calculate_aircraft_experience(self.level)
        self.upgrades = Aircraft.UpgradesRecord()
        self.scrap_got = 0

    def apply_wind(self, windmanager):
        self.wind_x, self.wind_y = windmanager.direction
        self.wind_x *= 80
        self.wind_y *= 80

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
        self.x += (self.ax + self.wind_x) * secs
        self.y += (self.ay + self.wind_y) * secs
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
            shoot_sfx.play()
            if self.upgrades.upgrade_branch == DOUBLE_CANNON_BRANCH:
                Bullet(self.x + cos(self.angle + 90) * 15, self.y + sin(self.angle + 90) * 15,
                       self.angle, self.upgrades.calculate_base_dmg() * (1.5 if self.upgrades[0] >= 3 else 1),
                       BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                Bullet(self.x + cos(self.angle - 90) * 15, self.y + sin(self.angle - 90) * 15,
                       self.angle, self.upgrades.calculate_base_dmg() * (1.5 if self.upgrades[0] >= 3 else 1),
                       BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                if self.upgrades[0] >= 1:
                    Bullet(self.x, self.y, self.angle,
                           self.upgrades.calculate_base_dmg() * (2 if self.upgrades[0] >= 2 else 1),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
            elif self.upgrades.upgrade_branch == MINIGUN_CANNON_BRANCH:
                if self.upgrades[0] >= 1:
                    Bullet(self.x + cos(self.angle + 90) * 15, self.y + sin(self.angle + 90) * 15,
                           self.angle, self.upgrades.calculate_base_dmg(),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                    Bullet(self.x + cos(self.angle - 90) * 15, self.y + sin(self.angle - 90) * 15,
                           self.angle, self.upgrades.calculate_base_dmg(),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                if self.upgrades[0] != 1:
                    Bullet(self.x, self.y, self.angle,
                           self.upgrades.calculate_base_dmg() * (2 if self.upgrades[0] >= 3 else 1),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
            elif self.upgrades.upgrade_branch == HEAVY_CANNON_BRANCH:
                if self.upgrades[0] >= 1:
                    Bullet(self.x + cos(self.angle + 90) * 15, self.y + sin(self.angle + 90) * 15,
                           self.angle, self.upgrades.calculate_base_dmg() * (2 if self.upgrades[0] >= 2 else 1),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                    Bullet(self.x + cos(self.angle - 90) * 15, self.y + sin(self.angle - 90) * 15,
                           self.angle, self.upgrades.calculate_base_dmg() * (2 if self.upgrades[0] >= 2 else 1),
                           BULLET_SPEED, groups["player_bullets"], groups["sprites"])
                Bullet(self.x, self.y, self.angle,
                       self.upgrades.calculate_base_dmg() * (3 if self.upgrades[0] >= 3 else 1),
                       BULLET_SPEED, groups["player_bullets"], groups["sprites"])
            else:
                Bullet(self.x, self.y, self.angle, self.upgrades.calculate_base_dmg(),
                       BULLET_SPEED, groups["player_bullets"], groups["sprites"])
            self.cooldown = self.upgrades.calculate_cooldown()

    def check_bullet_collisions(self, groups):
        """Проверяет столкновение с пулями."""
        bullet = pygame.sprite.spritecollideany(self, groups["enemy_bullets"],
                                                collided=pygame.sprite.collide_rect_ratio(.5))
        if bullet is not None and isinstance(bullet, Bullet):
            explode_sfx.play()
            self.hp -= bullet.dmg
            Explosion(self.x, self.y, groups["sprites"], groups["explosions"])
            bullet.kill()

    def check_drops(self, groups):
        drop = pygame.sprite.spritecollideany(self, groups["drops"],
                                              collided=pygame.sprite.collide_rect_ratio(.75))
        if drop is not None:
            if isinstance(drop, Experience):
                self.experience += drop.xp
                coin_sfx.play()
            elif isinstance(drop, Scrap):
                self.scrap_got += 1
                coin_sfx.play()
            elif isinstance(drop, HealthRefill):
                self.hp += 1 if self.hp < self.max_hp else 0
                heart_sfx.play()
            drop.kill()
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
