"""Класс спрайта кнопки с текстом, используюейся в процессе улучшения."""
import pygame
from const import FONT_FILE


class UpgradeButton(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, text, *groups):
        super().__init__(*groups)
        self.value = 0
        self.image = pygame.Surface((w, h))
        self.text = text
        pygame.draw.rect(self.image, "white", (1, 1, w - 2, h - 2), 0)
        lines = text.split("\n")
        rendered = list(map(lambda textline: pygame.font.Font(FONT_FILE, 18).render(textline, True, "black"), lines))
        total_height = sum(map(lambda textline: textline.get_height(), rendered))
        line_height = total_height // len(lines)
        start_height = (h - total_height) // 2
        for i, line in enumerate(rendered):
            self.image.blit(line, ((w - line.get_width()) // 2, start_height + line_height * i))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left, self.rect.top = self.x, self.y
