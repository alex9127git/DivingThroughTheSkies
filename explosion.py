"""Класс анимированного спрайта взрыва."""
import pygame
import rendering


SECONDS_PER_FRAME = 0.125


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups, is_long=False):
        super().__init__(*groups)
        self.frames = []
        self.sheet = rendering.load_image("explosion 4x1.png", colorkey=-1)
        self.cut_sheet(self.sheet, 4, 1)
        self.frame = 0
        self.image = self.frames[self.frame]
        self.x, self.y = x, y
        self.rect.center = self.x, self.y
        self.elapsed_time = 0
        self.seconds_per_frame = SECONDS_PER_FRAME * (10 if is_long else 1)

    def cut_sheet(self, sheet, columns, rows):
        """Генерирует кадры взрыва."""
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, secs):
        self.elapsed_time += secs
        if self.elapsed_time < self.seconds_per_frame * 4:
            self.frame = int(self.elapsed_time // self.seconds_per_frame)
            self.image = self.frames[self.frame]
            self.rect.center = self.x, self.y
        else:
            self.kill()

    def kill(self):
        super().kill()
        del self
