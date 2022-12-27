"""Главный файл программы."""
from random import randrange

import pygame
from aircraft import Aircraft
from const import COOLDOWN, calculate_enemies, calculate_difficulty, calculate_enemy_spawn_timer, \
    calculate_simultaneous_enemies, calculate_fighter_chance, AIRCRAFT_HP, WIDTH
from cursor import Cursor
from drone import Drone
from enemy import Enemy
from fighter import Fighter
from rendering import initialize
from bar import Bar
from text import Text


def run():
    """Запускает игру."""
    screen = initialize()
    # генерация групп
    sprites = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ui = pygame.sprite.Group()
    groups = {"sprites": sprites, "explosions": explosions, "player_bullets": player_bullets,
              "enemy_bullets": enemy_bullets, "enemies": enemies, "ui": ui}
    # генерация начальных спрайтов
    aircraft = Aircraft(sprites)
    cursor = Cursor(sprites, ui)
    hpBar = Bar(10, 10, AIRCRAFT_HP, "green", sprites, ui)
    cooldownBar = Bar(10, 40, COOLDOWN, "black", sprites, ui)
    stageText = Text("Stage 1", "black", WIDTH - 10, 10, "topright", sprites, ui)
    # генерация переменных игры
    stage = 1
    difficulty = calculate_difficulty(stage)
    enemies_defeated = 0
    enemies_to_next_stage = calculate_enemies(stage)
    enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
    timer = enemy_spawn_timer
    simultaneous_enemies = calculate_simultaneous_enemies(stage)
    game_over_timer = 0
    # игровой цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                aircraft.shoot(groups)
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
        # проверяем, жив ли самолет. Если нет, игра выключается через 1.5 секунд
        if not aircraft.alive():
            game_over_timer += secs
            if game_over_timer >= 1.5:
                running = False
        timer -= secs
        # если враги могут появиться, генерируем их
        if len(enemies) < simultaneous_enemies and timer <= 0:
            if randrange(100) < calculate_fighter_chance(stage):
                Fighter(difficulty, aircraft, enemies, sprites)
            else:
                Drone(difficulty, enemies, sprites)
            timer = enemy_spawn_timer
        # проверки, связанные с поведением врагов
        for enemy in enemies.sprites():
            if isinstance(enemy, Enemy):
                if enemy.check_bullet_collisions(groups):
                    enemies_defeated += 1
                else:
                    enemy.check_aircraft_collisions(aircraft, groups)
                if isinstance(enemy, Fighter):
                    enemy.update_strategy(aircraft, groups)
        aircraft.rotate_to_cursor(cursor)
        aircraft.check_bullet_collisions(groups)
        stageText.update_text(f"Stage {stage}")
        cooldownBar.update_value(COOLDOWN - aircraft.cooldown)
        hpBar.update_value(aircraft.hp)
        sprites.update(secs)
        if enemies_defeated >= enemies_to_next_stage:
            stage += 1
            difficulty = calculate_difficulty(stage)
            enemies_defeated -= enemies_to_next_stage
            enemies_to_next_stage = calculate_enemies(stage)
            enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
            simultaneous_enemies = calculate_simultaneous_enemies(stage)
        sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()
