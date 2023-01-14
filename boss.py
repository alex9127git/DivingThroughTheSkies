"""Класс спрайта самолета-босса."""
import pygame
from random import randint, random

from bullet import Bullet
from cannon import Cannon
from const import WIDTH, calculate_scrap_drop_chance, shoot_sfx, explode_sfx, boss_defeated_sfx
from enemy import Enemy

from explosion import Explosion
from fighter import Fighter
from health_refill import HealthRefill
from scrap import Scrap


class Boss(Enemy):
    def __init__(self, difficulty, *groups):
        super().__init__("boss", difficulty, *groups)
        self.x, self.y = WIDTH // 2, -self.image.get_height() // 2
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.hp = int(5 * self.difficulty)
        self.max_hp = self.hp
        self.bullet_dmg = 1
        self.experience_dropped = randint(int(30 * self.difficulty), int(50 * self.difficulty))
        self.scrap_drop_chance = calculate_scrap_drop_chance(self.difficulty) * 100
        self.guaranteed_scraps = int(self.scrap_drop_chance // 100)
        self.scrap_drop_chance %= 100
        self.cannons = [
            Cannon(self, 0, -25, difficulty, "radial cannon",
                   int(12 * self.difficulty ** (1 + (self.difficulty - 1) / 4)), *groups),
            Cannon(self, -120, -25, difficulty, "cannon",
                   int(7 * self.difficulty ** (1 + (self.difficulty - 1) / 4)), *groups),
            Cannon(self, 120, -25, difficulty, "cannon",
                   int(7 * self.difficulty ** (1 + (self.difficulty - 1) / 4)), *groups),
            Cannon(self, -240, -45, difficulty, "cannon",
                   int(7 * self.difficulty ** (1 + (self.difficulty - 1) / 4)), *groups),
            Cannon(self, 240, -45, difficulty, "cannon",
                   int(7 * self.difficulty ** (1 + (self.difficulty - 1) / 4)), *groups),
        ]
        self.shoot_cooldown = 5 / round(self.difficulty, 1)
        self.timer = self.shoot_cooldown
        self.ability = 1
        self.ability_cooldown = 30 / round(self.difficulty, 1)
        self.ability_timer = self.ability_cooldown
        self.shortened_shots = 0

    def update(self, secs):
        if self.y <= 100:
            self.y += 100 * secs
        self.rect.center = self.x, self.y
        self.timer -= secs
        self.ability_timer -= secs
        dead_cannons = []
        for cannon in self.cannons:
            if not cannon.alive():
                dead_cannons.append(cannon)
        for dead_cannon in dead_cannons:
            self.cannons.remove(dead_cannon)

    def check_aircraft_collisions(self, aircraft, groups):
        """Проверяет столкновение с самолетом игрока."""
        pass

    def check_bullet_collisions(self, groups):
        """Проверяет столкновение с пулями."""
        if len(self.cannons) == 0:
            bullet = pygame.sprite.spritecollideany(self, groups["player_bullets"],
                                                    collided=pygame.sprite.collide_rect_ratio(.25))
            if bullet is not None and isinstance(bullet, Bullet):
                self.hp -= bullet.dmg
                bullet.kill()
                if self.hp <= 0:
                    boss_defeated_sfx.play()
                    explode_sfx.play()
                    for _ in range(20):
                        Explosion(self.x + randint(-150, 150), self.y + randint(-150, 150),
                                  groups["sprites"], groups["explosions"], is_long=True)
                    self.generate_experience(groups)
                    for _ in range(self.guaranteed_scraps):
                        Scrap(self.x, self.y, groups["sprites"], groups["drops"])
                    if random() * 100 < self.scrap_drop_chance:
                        Scrap(self.x, self.y, groups["sprites"], groups["drops"])
                    for _ in range(3):
                        HealthRefill(self.x, self.y, groups["sprites"], groups["drops"])
                    self.kill()
                    return True
        return False

    def update_strategy(self, aircraft, groups):
        for cannon in self.cannons:
            if isinstance(cannon, Cannon):
                if cannon.cannon_type == "cannon":
                    cannon.track(aircraft)
                elif cannon.cannon_type == "radial cannon":
                    cannon.angle -= 1
        if self.timer <= 0:
            shoot_sfx.play()
            self.timer = 0.2 if self.shortened_shots else self.shoot_cooldown
            self.shortened_shots -= 1 if self.shortened_shots else 0
            for cannon in self.cannons:
                cannon.shoot(groups)
        if self.ability_timer <= 0:
            self.ability_timer = self.ability_cooldown
            if self.ability == 1:
                self.shortened_shots = 3
                self.timer = 0.2
            elif self.ability == 2:
                Fighter(self.difficulty, aircraft, groups["enemies"], groups["sprites"])
            self.ability = randint(1, 2)
