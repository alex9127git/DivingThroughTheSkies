"""Общий класс, использующийся для спрайтов врагов."""
from random import randrange
import pygame
from bullet import Bullet
from experience import Experience
from explosion import Explosion
from rendering import load_image


class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemy_type, difficulty, *groups):
        super().__init__(*groups)
        self.orig = pygame.transform.scale(load_image(f"{enemy_type}.png", colorkey=-1), (50, 50))
        self.x = 0
        self.y = 0
        self.angle = 0
        self.image = pygame.transform.rotate(self.orig, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.difficulty = difficulty
        self.hp = 1
        self.dmg = 1
        self.experience_dropped = 0

    def update(self, secs):
        pass

    def check_bullet_collisions(self, groups):
        """Проверяет столкновение с пулями."""
        bullet = pygame.sprite.spritecollideany(self, groups["player_bullets"],
                                                collided=pygame.sprite.collide_rect_ratio(.75))
        if bullet is not None and isinstance(bullet, Bullet):
            self.hp -= bullet.dmg
            bullet.kill()
            if self.hp <= 0:
                Explosion(self.x, self.y, groups["sprites"], groups["explosions"])
                self.generate_experience(groups)
                self.kill()
                return True
        return False

    def check_aircraft_collisions(self, aircraft, groups):
        """Проверяет столкновение с самолетом игрока."""
        if pygame.sprite.spritecollideany(aircraft, groups["enemies"],
                                          collided=pygame.sprite.collide_rect_ratio(.5)) == self:
            if aircraft.hp > 0:
                aircraft.hp -= self.dmg
                Explosion(aircraft.x, aircraft.y, groups["sprites"], groups["explosions"])
            self.kill()

    def generate_experience(self, groups):
        gold_xp = self.experience_dropped // 25
        silver_xp = (self.experience_dropped % 25) // 5
        bronze_xp = self.experience_dropped % 5
        for _ in range(gold_xp):
            Experience(self.x, self.y, 25, groups["sprites"], groups["experience_coins"])
        for _ in range(silver_xp):
            Experience(self.x, self.y, 5, groups["sprites"], groups["experience_coins"])
        for _ in range(bronze_xp):
            Experience(self.x, self.y, 1, groups["sprites"], groups["experience_coins"])

    def kill(self):
        super().kill()
        del self