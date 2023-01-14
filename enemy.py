"""Общий класс, использующийся для спрайтов врагов."""
import pygame
import bullet
import rendering
from experience import Experience
from explosion import Explosion
from health_refill import HealthRefill
from const import calculate_scrap_drop_chance, calculate_health_refill_drop_chance, explode_sfx
from random import random
from scrap import Scrap


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, difficulty, *groups):
        super().__init__(*groups)
        self.orig = rendering.load_image(f"{enemy_type}.png", colorkey=-1)
        self.x = 0
        self.y = 0
        self.angle = 0
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.difficulty = difficulty
        self.hp = 1
        self.max_hp = self.hp
        self.dmg = 1
        self.experience_dropped = 0
        self.scrap_drop_chance = calculate_scrap_drop_chance(self.difficulty)
        self.guaranteed_scraps = int(self.scrap_drop_chance // 100)
        self.scrap_drop_chance %= 100

    def update(self, secs):
        pass

    def check_bullet_collisions(self, groups):
        """Проверяет столкновение с пулями."""
        b = pygame.sprite.spritecollideany(self, groups["player_bullets"],
                                           collided=pygame.sprite.collide_rect_ratio(.75))
        if b is not None and isinstance(b, bullet.Bullet):
            self.hp -= b.dmg
            b.kill()
            if self.hp <= 0:
                explode_sfx.play()
                Explosion(self.x, self.y, groups["sprites"], groups["explosions"])
                self.generate_experience(groups)
                for _ in range(self.guaranteed_scraps):
                    Scrap(self.x, self.y, groups["sprites"], groups["drops"])
                if random() * 100 < self.scrap_drop_chance:
                    Scrap(self.x, self.y, groups["sprites"], groups["drops"])
                if random() * 100 < calculate_health_refill_drop_chance():
                    HealthRefill(self.x, self.y, groups["sprites"], groups["drops"])
                self.kill()
                return True
        return False

    def check_aircraft_collisions(self, aircraft, groups):
        """Проверяет столкновение с самолетом игрока."""
        if pygame.sprite.spritecollideany(aircraft, groups["enemies"],
                                          collided=pygame.sprite.collide_rect_ratio(.5)) == self:
            if aircraft.hp > 0:
                explode_sfx.play()
                aircraft.hp -= self.dmg
                Explosion(aircraft.x, aircraft.y, groups["sprites"], groups["explosions"])
            self.kill()

    def generate_experience(self, groups):
        gold_xp = self.experience_dropped // 25
        silver_xp = (self.experience_dropped % 25) // 5
        bronze_xp = self.experience_dropped % 5
        for _ in range(gold_xp):
            Experience(self.x, self.y, 25, groups["sprites"], groups["drops"])
        for _ in range(silver_xp):
            Experience(self.x, self.y, 5, groups["sprites"], groups["drops"])
        for _ in range(bronze_xp):
            Experience(self.x, self.y, 1, groups["sprites"], groups["drops"])

    def kill(self):
        super().kill()
        del self
