"""Класс спрайта монет опыта."""
import pygame
from drop import Drop
import rendering


class Experience(Drop):
    def __init__(self, x, y, xp_value, *groups):
        super().__init__(x, y, *groups)
        self.image = pygame.transform.scale(rendering.load_image(f"{xp_value}xp.png", colorkey=-1), (20, 20))
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.xp = xp_value

    def update(self, secs):
        self.x += self.ax * secs
        self.y += self.ay * secs
        self.ax *= 0.99
        self.ay *= 0.99
        if abs(self.ax) <= 1:
            self.ax = 0
        if abs(self.ay) <= 1:
            self.ay = 0
        self.rect.center = self.x, self.y

    def kill(self):
        super().kill()
        del self
