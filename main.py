import pygame
from aircraft import Aircraft
from cursor import Cursor
from rendering import initialize


screen = initialize()
sprites = pygame.sprite.Group()
aircraft = Aircraft(sprites)
cursor = Cursor(sprites)


running = True
clock = pygame.time.Clock()
secs = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            cursor.update_pos(*event.pos)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            aircraft.accelerate(3, 0)
        if keys[pygame.K_a]:
            aircraft.accelerate(-3, 0)
        if keys[pygame.K_s]:
            aircraft.accelerate(0, 3)
        if keys[pygame.K_w]:
            aircraft.accelerate(0, -3)
    screen.fill("white")
    secs = clock.tick(60) / 1000
    aircraft.update(secs, cursor)
    cursor.update(secs)
    sprites.draw(screen)
    pygame.display.flip()
pygame.quit()
