"""Главный файл программы."""
import sys
from random import randrange
import pygame
from aircraft import Aircraft
from boss import Boss
from const import calculate_enemies, calculate_difficulty, calculate_enemy_spawn_timer, \
    calculate_simultaneous_enemies, calculate_fighter_chance, AIRCRAFT_HP, WIDTH, HEIGHT, INITIAL_SPLIT_PATH, \
    DOUBLE_CANNON_UPGRADES, MINIGUN_CANNON_UPGRADES, HEAVY_CANNON_UPGRADES, MINIGUN_CANNON_BRANCH, \
    DOUBLE_CANNON_BRANCH, HEAVY_CANNON_BRANCH, FONT_FILE, is_boss_stage
from cursor import Cursor
from drone import Drone
from enemy import Enemy
from fighter import Fighter
from rendering import initialize, load_image
from bar import Bar
from text import Text
from upgrade import UpgradeButton
from file_func import get_upgrades_data, update_upgrades_data


def terminate():
    """Terminates the program. Used when player closes the game window manually."""
    pygame.quit()
    sys.exit()


def main_menu(screen):
    play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 75, 200, 50)
    upgrades_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(*event.pos):
                    return "play"
                elif upgrades_button.collidepoint(*event.pos):
                    return "upgrades"
        screen.fill((128, 192, 255))
        text = pygame.font.Font(FONT_FILE, 36).render("Diving Through the Skies", True, "black")
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2 - 100))
        pygame.draw.rect(screen, "white", play_button, 0)
        pygame.draw.rect(screen, "black", play_button, 3)
        play = pygame.font.Font(FONT_FILE, 24).render("ИГРАТЬ", True, "black")
        screen.blit(play, (play_button.left + play_button.width // 2 - play.get_width() // 2,
                           play_button.top + play_button.height // 2 - play.get_height() // 2))
        pygame.draw.rect(screen, "white", upgrades_button, 0)
        pygame.draw.rect(screen, "black", upgrades_button, 3)
        upgrades = pygame.font.Font(FONT_FILE, 24).render("УЛУЧШЕНИЯ", True, "black")
        screen.blit(upgrades, (upgrades_button.left + upgrades_button.width // 2 - upgrades.get_width() // 2,
                               upgrades_button.top + upgrades_button.height // 2 - upgrades.get_height() // 2))
        pygame.display.flip()


def game(screen):
    """Запускает игру."""
    # генерация групп
    sprites = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    drops = pygame.sprite.Group()
    player_bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    ui = pygame.sprite.Group()
    upgrade_ui = pygame.sprite.Group()
    scrap_image = pygame.transform.scale(load_image(f"scrap1.png", colorkey=-1), (25, 25))
    Text("Выберите улучшение из трёх", "black", 20, 20, "topleft", upgrade_ui)
    groups = {"sprites": sprites, "explosions": explosions, "drops": drops,
              "player_bullets": player_bullets, "enemy_bullets": enemy_bullets, "enemies": enemies, "ui": ui,
              "upgrade_ui": upgrade_ui}
    # генерация начальных спрайтов
    aircraft = Aircraft(sprites)
    cursor = Cursor(sprites, ui)
    hp_bar = Bar(20, 20, 100, 20, AIRCRAFT_HP, "green", sprites, ui)
    cooldown_bar = Bar(20, 50, 100, 20, aircraft.upgrades.calculate_cooldown(), "black", sprites, ui)
    xp_bar = Bar(20, HEIGHT - 40, WIDTH - 40, 20, aircraft.experience_to_next_level, (240, 148, 80), sprites, ui)
    stage_text = Text("Сложность: 1", "black", WIDTH - 20, 20, "topright", sprites, ui)
    scrap_got_text = Text("0", "black", WIDTH - 20, 60, "topright", sprites, ui)
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
    boss_defeated = False
    paused = False
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                cursor.update_pos(*event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if leveling_up == -1:
                    aircraft.shoot(groups)
                else:
                    button_pressed = -1
                    if button1.rect.collidepoint(*event.pos):
                        button_pressed = DOUBLE_CANNON_BRANCH
                    elif button2.rect.collidepoint(*event.pos):
                        button_pressed = MINIGUN_CANNON_BRANCH
                    elif button3.rect.collidepoint(*event.pos):
                        button_pressed = HEAVY_CANNON_BRANCH
                    if button_pressed != -1:
                        if not aircraft.has_branch():
                            aircraft.assign_branch(button_pressed)
                            leveling_up = -1
                        else:
                            if (button1, button2, button3)[button_pressed].text != "":
                                aircraft.upgrades += button_pressed
                                leveling_up = -1
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                aircraft.accelerate(5, 0)
            if keys[pygame.K_a]:
                aircraft.accelerate(-5, 0)
            if keys[pygame.K_s]:
                aircraft.accelerate(0, 5)
            if keys[pygame.K_w]:
                aircraft.accelerate(0, -5)
            if pygame.mouse.get_pressed(3)[0] and aircraft.upgrades.upgrade_branch == MINIGUN_CANNON_BRANCH:
                aircraft.shoot(groups)
        screen.fill((128, 192, 255))
        secs = clock.tick(60) / 1000
        if leveling_up == -1 and not paused:
            # проверяем, жив ли самолет. Если нет, игра выключается через 1.5 секунд
            if not aircraft.alive():
                game_over_timer += secs
                if game_over_timer >= 1.5:
                    running = False
            timer -= secs
            # если враги могут появиться, генерируем их
            if len(enemies) < simultaneous_enemies and timer <= 0:
                if is_boss_stage(stage):
                    if len(enemies) == 0:
                        Boss(difficulty, enemies, sprites)
                else:
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
                    if isinstance(enemy, Boss):
                        boss_defeated = enemy.hp <= 0
                        enemy.update_strategy(aircraft, groups)
            # проверки, связанные с самолетом
            aircraft.rotate_to_cursor(cursor)
            aircraft.check_bullet_collisions(groups)
            leveling_up = aircraft.check_drops(groups)
            if leveling_up != -1:
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
            stage_text.update_text(f"Сложность: {stage}")
            scrap_got_text.update_text(str(aircraft.scrap_got))
            cooldown_bar.update_value(aircraft.upgrades.calculate_cooldown() - aircraft.cooldown)
            cooldown_bar.update_max_value(aircraft.upgrades.calculate_cooldown())
            hp_bar.update_value(aircraft.hp)
            xp_bar.update_value(aircraft.experience)
            xp_bar.update_max_value(aircraft.experience_to_next_level)
            # вызов метода update у спрайтов
            sprites.update(secs)
            screen.blit(scrap_image, (scrap_got_text.rect.left - 10 - scrap_image.get_width(),
                                      scrap_got_text.rect.top))
            # пересчет параметров для следующего уровня сложности
            if enemies_defeated >= enemies_to_next_stage and not is_boss_stage(stage):
                stage += 1
                difficulty = calculate_difficulty(stage)
                enemies_defeated -= enemies_to_next_stage
                enemies_to_next_stage = calculate_enemies(stage)
                enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
                simultaneous_enemies = calculate_simultaneous_enemies(stage)
            if boss_defeated and is_boss_stage(stage):
                stage += 1
                difficulty = calculate_difficulty(stage)
                enemies_defeated = 0
                enemies_to_next_stage = calculate_enemies(stage)
                enemy_spawn_timer = calculate_enemy_spawn_timer(stage)
                simultaneous_enemies = calculate_simultaneous_enemies(stage)
            # отрисовка спрайтов
            sprites.draw(screen)
            ui.draw(screen)
        elif leveling_up != -1:
            # отрисовка спрайтов
            upgrade_ui.update(secs)
            upgrade_ui.draw(screen)
        elif paused:
            pause_text = pygame.font.Font(FONT_FILE, 48).render("ПАУЗА", True, "black")
            screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2,
                                     HEIGHT // 2 - pause_text.get_height() // 2))
        pygame.display.flip()
    return aircraft.scrap_got, stage, aircraft.level


def stats(screen, scrap, stage, level):
    screen.fill((128, 192, 255))
    scrap_image = pygame.transform.scale(load_image(f"scrap1.png", colorkey=-1), (25, 25))
    bigger_scrap_image = pygame.transform.scale(load_image(f"scrap1.png", colorkey=-1), (50, 50))
    game_over_text = pygame.font.Font(FONT_FILE, 36).render("ИГРА ОКОНЧЕНА", True, "black")
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, 100))
    scrap_text = pygame.font.Font(FONT_FILE, 24).render("Металлолома за уровень самолета:", True, "black")
    screen.blit(scrap_text, (20, 200))
    qty_text = pygame.font.Font(FONT_FILE, 24).render(str(level * 5), True, "black")
    screen.blit(qty_text, (WIDTH - 20 - qty_text.get_width(), 200))
    screen.blit(scrap_image, (WIDTH - 30 - qty_text.get_width() - scrap_image.get_width(), 200))
    scrap_text = pygame.font.Font(FONT_FILE, 24).render("Металлолома c врагов:", True, "black")
    screen.blit(scrap_text, (20, 250))
    qty_text = pygame.font.Font(FONT_FILE, 24).render(str(scrap), True, "black")
    screen.blit(qty_text, (WIDTH - 20 - qty_text.get_width(), 250))
    screen.blit(scrap_image, (WIDTH - 30 - qty_text.get_width() - scrap_image.get_width(), 250))
    scrap_text = pygame.font.Font(FONT_FILE, 24).render("Коэффициент сложности:", True, "black")
    screen.blit(scrap_text, (20, 300))
    qty_text = pygame.font.Font(FONT_FILE, 24).render(f"x{calculate_difficulty(stage) ** 2:.2f}", True, "black")
    screen.blit(qty_text, (WIDTH - 20 - qty_text.get_width(), 300))
    scrap_text = pygame.font.Font(FONT_FILE, 48).render("Всего:", True, "black")
    total = int((level * 5 + scrap) * calculate_difficulty(stage) ** 2)
    screen.blit(scrap_text, (20, 350))
    qty_text = pygame.font.Font(FONT_FILE, 48).render(str(total), True, "black")
    screen.blit(qty_text, (WIDTH - 20 - qty_text.get_width(), 350))
    screen.blit(bigger_scrap_image, (WIDTH - 30 - qty_text.get_width() - bigger_scrap_image.get_width(), 350))
    button = pygame.Rect(WIDTH // 2 - 150, 450, 300, 50)
    pygame.draw.rect(screen, "white", button, 0)
    pygame.draw.rect(screen, "black", button, 3)
    play = pygame.font.Font(FONT_FILE, 24).render("ГЛАВНЫЙ ЭКРАН", True, "black")
    screen.blit(play, (button.left + button.width // 2 - play.get_width() // 2,
                       button.top + button.height // 2 - play.get_height() // 2))
    upgrades_data = get_upgrades_data()
    upgrades_data["scrap"] += total
    update_upgrades_data(upgrades_data)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(*event.pos):
                    running = False
        pygame.display.flip()


def upgrades_screen(screen):
    button = pygame.Rect(WIDTH // 2 - 100, 700, 200, 50)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(*event.pos):
                    running = False
        screen.fill((128, 192, 255))
        pygame.draw.rect(screen, "white", button, 0)
        pygame.draw.rect(screen, "black", button, 3)
        back = pygame.font.Font(FONT_FILE, 24).render("НАЗАД", True, "black")
        screen.blit(back, (button.left + button.width // 2 - back.get_width() // 2,
                           button.top + button.height // 2 - back.get_height() // 2))
        pygame.display.flip()


def run():
    screen = initialize()
    while True:
        button_pressed = main_menu(screen)
        if button_pressed == "play":
            scrap, stage, level = game(screen)
            stats(screen, scrap, stage, level)
        elif button_pressed == "upgrades":
            upgrades_screen(screen)


if __name__ == "__main__":
    run()
