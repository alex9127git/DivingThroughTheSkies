"""Класс, позволяющий отрисовывать различный текст."""
import pygame
from const import FONT_FILE


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, x, y, pivot, *groups):
        super().__init__(*groups)
        self.text = text
        self.color = color
        self.x = x
        self.y = y
        self.pivot = pivot

    def update(self, secs):
        self.image = pygame.font.Font(FONT_FILE, 24).render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        coords = self.x, self.y
        if self.pivot == "topleft":
            self.rect.topleft = coords
        if self.pivot == "topright":
            self.rect.topright = coords
        if self.pivot == "bottomleft":
            self.rect.bottomleft = coords
        if self.pivot == "bottomright":
            self.rect.bottomright = coords

    def update_text(self, text):
        """Обновляет отображаемый текст."""
        self.text = text
