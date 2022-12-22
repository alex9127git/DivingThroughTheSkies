import pygame
from aircraft import Aircraft
from const import COOLDOWN
from cursor import Cursor
from rendering import initialize
from cooldownbar import CooldownBar


def run():
    screen = initialize()
    sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    aircraft = Aircraft(sprites)
    cursor = Cursor(sprites)
    cooldownBar = CooldownBar(10, 10, COOLDOWN, sprites)

    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                aircraft.shoot(bullets, sprites)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                aircraft.accelerate(3, 0)
            if keys[pygame.K_a]:
                aircraft.accelerate(-3, 0)
            if keys[pygame.K_s]:
                aircraft.accelerate(0, 3)
            if keys[pygame.K_w]:
                aircraft.accelerate(0, -3)
        screen.fill((128, 192, 255))
        secs = clock.tick(60) / 1000
        aircraft.update(secs, cursor)
        cursor.update(secs)
        bullets.update(secs)
        cooldownBar.update(COOLDOWN - aircraft.cooldown)
        sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()
