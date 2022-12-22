import pygame


class CooldownBar(pygame.sprite.Sprite):
    def __init__(self, x, y, max_value, *groups):
        super().__init__(*groups)
        self.max_value = max_value
        self.value = 0
        self.image = pygame.Surface((100, 20))
        self.image.fill("white")
        pygame.draw.rect(self.image, "black", self.image.get_rect(), 1)
        pygame.draw.rect(self.image, "black",
                         (0, 0, self.image.get_width() / self.max_value * self.value, self.image.get_height()), 0)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.left, self.rect.top = self.x, self.y

    def update(self, value):
        self.value = value
        self.image.fill("white")
        pygame.draw.rect(self.image, "black", self.image.get_rect(), 1)
        pygame.draw.rect(self.image, "black",
                         (0, 0, self.image.get_width() / self.max_value * self.value, self.image.get_height()), 0)
