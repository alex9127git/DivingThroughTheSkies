"""Главный файл программы."""
from random import randrange

import pygame
from aircraft import Aircraft
from const import COOLDOWN, calculate_enemies, calculate_difficulty, calculate_enemy_spawn_timer, \
    calculate_simultaneous_enemies, calculate_fighter_chance, AIRCRAFT_HP, WIDTH, HEIGHT, INITIAL_SPLIT_PATH, \
    DOUBLE_CANNON_UPGRADES, MINIGUN_CANNON_UPGRADES, HEAVY_CANNON_UPGRADES
from cursor import Cursor
from drone import Drone
from enemy import Enemy
from fighter import Fighter
from rendering import initialize
from bar import Bar
from text import Text
from upgrade import UpgradeButton


def run():
    """Запускает игру."""
    screen = initialize()
    # генерация групп
    sprites = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    experience_coins = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ui = pygame.sprite.Group()
    upgrade_ui = pygame.sprite.Group()
    Text("Выберите улучшение из трёх", "black", 20, 20, "topleft", upgrade_ui)
    groups = {"sprites": sprites, "explosions": explosions, "experience_coins": experience_coins,
              "player_bullets": player_bullets, "enemy_bullets": enemy_bullets, "enemies": enemies, "ui": ui,
              "upgrade_ui": upgrade_ui}
    # генерация начальных спрайтов
    aircraft = Aircraft(sprites)
    cursor = Cursor(sprites, ui)
    hpBar = Bar(20, 20, 100, 20, AIRCRAFT_HP, "green", sprites, ui)
    cooldownBar = Bar(20, 50, 100, 20, COOLDOWN, "black", sprites, ui)
    xpBar = Bar(20, HEIGHT - 40, WIDTH - 40, 20, aircraft.experience_to_next_level, (240, 148, 80), sprites, ui)
    stageText = Text("Сложность: 1", "black", WIDTH - 20, 20, "topright", sprites, ui)
    # генерация переменных игры
    stage = 1
    difficulty = calculate_difficulty(stage)
    enemies_defeated = 0
    enemies_to_next_stage = calculate_enemies(stage)
    enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
    timer = enemy_spawn_timer
    simultaneous_enemies = calculate_simultaneous_enemies(stage)
    game_over_timer = 0
    button1 = None
    button2 = None
    button3 = None
    # игровой цикл
    leveling_up = -1
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if leveling_up == -1:
                    aircraft.shoot(groups)
                else:
                    button_pressed = -1
                    if button1.rect.collidepoint(*event.pos):
                        button_pressed = 0
                    elif button2.rect.collidepoint(*event.pos):
                        button_pressed = 1
                    elif button3.rect.collidepoint(*event.pos):
                        button_pressed = 2
                    if button_pressed != -1:
                        if not aircraft.has_branch():
                            aircraft.assign_branch(button_pressed)
                            leveling_up = -1
                        else:
                            if (button1, button2, button3)[button_pressed].text != "":
                                aircraft.upgrades += button_pressed
                                leveling_up = -1
                                print(aircraft.upgrades.upgrades)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                aircraft.accelerate(5, 0)
            if keys[pygame.K_a]:
                aircraft.accelerate(-5, 0)
            if keys[pygame.K_s]:
                aircraft.accelerate(0, 5)
            if keys[pygame.K_w]:
                aircraft.accelerate(0, -5)
        screen.fill((128, 192, 255))
        secs = clock.tick(60) / 1000
        if leveling_up == -1:
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
            # проверки, связанные с самолетом
            aircraft.rotate_to_cursor(cursor)
            aircraft.check_bullet_collisions(groups)
            leveling_up = aircraft.check_experience(groups)
            if leveling_up != -1:
                for enemy in enemies:
                    enemy.kill()
                for bullet in enemy_bullets:
                    bullet.kill()
                if aircraft.has_branch():
                    branch = ((DOUBLE_CANNON_UPGRADES, MINIGUN_CANNON_UPGRADES, HEAVY_CANNON_UPGRADES)
                              [aircraft.upgrades.upgrade_branch])
                    text1 = branch[0][aircraft.upgrades[0]] if aircraft.upgrades[0] < 3 else ""
                    text2 = branch[1][aircraft.upgrades[1]] if aircraft.upgrades[1] < 5 else ""
                    text3 = branch[2][aircraft.upgrades[2]] if aircraft.upgrades[2] < 5 else ""
                else:
                    text1, text2, text3 = INITIAL_SPLIT_PATH
                button1 = UpgradeButton(20, 60, 240, 520, text1, upgrade_ui)
                button2 = UpgradeButton(280, 60, 240, 520, text2, upgrade_ui)
                button3 = UpgradeButton(540, 60, 240, 520, text3, upgrade_ui)
                continue
            # обновление графического интерфейса
            stageText.update_text(f"Сложность: {stage}")
            cooldownBar.update_value(COOLDOWN - aircraft.cooldown)
            hpBar.update_value(aircraft.hp)
            xpBar.update_value(aircraft.experience)
            xpBar.update_max_value(aircraft.experience_to_next_level)
            # вызов метода update у спрайтов
            sprites.update(secs)
            # пересчет параметров для следующего уровня сложности
            if enemies_defeated >= enemies_to_next_stage:
                stage += 1
                difficulty = calculate_difficulty(stage)
                enemies_defeated -= enemies_to_next_stage
                enemies_to_next_stage = calculate_enemies(stage)
                enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
                simultaneous_enemies = calculate_simultaneous_enemies(stage)
            # отрисовка спрайтов
            sprites.draw(screen)
        else:
            # отрисовка спрайтов
            upgrade_ui.update(secs)
            upgrade_ui.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    run()
