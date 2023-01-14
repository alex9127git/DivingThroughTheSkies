"""Класс, управляющий механикой ветра."""
from random import randrange, randint

import pygame
from const import WIDTH, HEIGHT


class WindManager(pygame.sprite.Sprite):
    class WindFlake:
        def __init__(self, x, y, r):
            self.x, self.y, self.r = x, y, r

        def apply_direction(self, direction):
            dx, dy = direction
            if dx == dy == 0:
                self.x += 0
                self.y += 1
            else:
                self.x += dx * 5
                self.y += dy * 5
            if self.x < 0:
                self.x = WIDTH
            if self.x > WIDTH:
                self.x = 0
            if self.y < 0:
                self.y = HEIGHT
            if self.y > HEIGHT:
                self.y = 0

    def __init__(self, *groups):
        super().__init__(*groups)
        self.enabled = False
        self.flakes = []
        for _ in range(200):
            self.flakes.append(WindManager.WindFlake(randrange(WIDTH), randrange(HEIGHT), randint(1, 3)))
        self.direction = (0, 0)
        self.timer = 10
        self.redraw()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
        self.direction = (0, 0)
        self.timer = 10

    def update(self, secs):
        if self.enabled:
            for flake in self.flakes:
                flake.apply_direction(self.direction)
            self.timer -= secs
            if self.timer <= 0:
                self.timer = randint(5, 10)
                self.direction = (randint(-1, 1), randint(-1, 1)) if self.direction == (0, 0) else (0, 0)
        self.redraw()

    def redraw(self):
        self.image = pygame.Surface((WIDTH, HEIGHT))
        self.image.set_colorkey("black")
        self.image.fill("black")
        if self.enabled:
            for flake in self.flakes:
                pygame.draw.circle(self.image, "white", (flake.x, flake.y), flake.r, 0)
        self.rect = self.image.get_rect()
        self.rect.center = WIDTH // 2, HEIGHT // 2
