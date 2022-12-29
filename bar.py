"""Класс спрайта различных полосок - здоровья, отката оружия и т.д."""
import pygame


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, max_value, color, *groups):
        super().__init__(*groups)
        self.max_value = max_value
        self.value = 0
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.color = color
        self.x = x
        self.y = y
        self.rect.left, self.rect.top = self.x, self.y

    def update(self, secs):
        self.image.fill("white")
        pygame.draw.rect(self.image, self.color,
                         (0, 0, self.image.get_width() / self.max_value * self.value, self.image.get_height()), 0)
        pygame.draw.rect(self.image, "black", self.image.get_rect(), 1)

    def update_max_value(self, value):
        """Обновляет максимальное значение полоски."""
        self.max_value = value

    def update_value(self, value):
        """Обновляет значение полоски."""
        self.value = value
