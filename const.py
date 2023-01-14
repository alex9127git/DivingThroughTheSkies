"""Класс, в котором хранятся все константы программы, а также функции, вычисляющие значения по формуле."""
import pygame
from file_func import get_upgrades_data

pygame.font.init()
pygame.mixer.init()
WIDTH = 800
HEIGHT = 600
MAX_ACCELERATION = 200
BULLET_SPEED = 500
AIRCRAFT_HP = 3
ENEMIES_START = 5
ENEMIES_INCREMENT = 1
SIMULTANEOUS_ENEMIES = 3
SIMULTANEOUS_ENEMIES_INCREMENT = 0.2
DIFFICULTY_START = 1.0
DIFFICULTY_INCREMENT = 0.2
ENEMY_SPAWN_TIMER = 3.0
ENEMY_SPAWN_TIMER_DECREMENT = 0.1
FIGHTER_CHANCE = 30
FIGHTER_CHANCE_INCREMENT = 5
EXPERIENCE_TO_LEVEL_UP = 100
EXPERIENCE_INCREMENT = 80
SCRAP_BASE_DROP_CHANCE = 1.0
SCRAP_DROP_CHANCE_INCREMENT = 0.2
HEALTH_BASE_DROP_CHANCE = 1.0
HEALTH_DROP_CHANCE_INCREMENT = 0.2
FONT_FILE = "data/AubreyPro.otf"

# Звуки
shoot_sfx = pygame.mixer.Sound("data/shoot.wav")
coin_sfx = pygame.mixer.Sound("data/coin.wav")
heart_sfx = pygame.mixer.Sound("data/heart.wav")
menu_select_sfx = pygame.mixer.Sound("data/select.wav")
explode_sfx = pygame.mixer.Sound("data/explosion.wav")

# улучшения
INITIAL_SPLIT_PATH = ["Двойная пушка:\nСтреляет двумя пулями\nрасположенными близко\nдруг к другу",
                      "Миниган:\nШаблон стрельбы\nнеизменный,\nперезарядка х0.33,\nпозволяет стрелять\nпри зажатой ЛКМ",
                      "Тяжелая пушка:\nПуля наносит 3 урона,\nперезарядка х1.5"]

DOUBLE_CANNON_BRANCH = 0
DOUBLE_CANNON_UPGRADES = [
    ["Модификация 1:\nТеперь выпускает\nтри пули\nвместо двух",
     "Модификация 2:\nЦентральная пуля наносит\nв 2 раза больше урона",
     "Сверхмодификация:\nБоковые пуля наносят\nв 1.5 раза больше урона"],
    ["Сильные пушки:\n+2 урона для всех пуль",
     "Сильные пушки:\n+2 урона для всех пуль",
     "Яростные пушки:\n+4 урона для всех пуль",
     "Яростные пушки:\n+4 урона для всех пуль",
     "Несравнимые пушки:\n+7 урона для всех пуль"],
    ["Быстрые пушки:\nвремя перезарядки x0.9",
     "Быстрые пушки:\nвремя перезарядки x0.9",
     "Скоростные пушки:\nвремя перезарядки х0.8",
     "Скоростные пушки:\nвремя перезарядки х0.8",
     "Сверхбыстрые пушки:\nвремя перезарядки x0.6"]
]

MINIGUN_CANNON_BRANCH = 1
MINIGUN_CANNON_UPGRADES = [
    ["Модификация 1:\nТеперь выпускает\nдве пули\nвместо одной",
     "Модификация 2:\nТеперь выпускает\nтри пули\nвместо двух",
     "Сверхмодификация:\nЦентральная пуля\nнаносит в 2 раза\nбольше урона"],
    ["Сильные пушки:\n+1 урона для всех пуль",
     "Сильные пушки:\n+1 урона для всех пуль",
     "Яростные пушки:\n+3 урона для всех пуль",
     "Яростные пушки:\n+3 урона для всех пуль",
     "Несравнимые пушки:\n+5 урона для всех пуль"],
    ["Быстрые пушки:\nвремя перезарядки x0.8",
     "Быстрые пушки:\nвремя перезарядки x0.8",
     "Скоростные пушки:\nвремя перезарядки х0.7",
     "Скоростные пушки:\nвремя перезарядки х0.7",
     "Сверхбыстрые пушки:\nвремя перезарядки x0.5"]
]

HEAVY_CANNON_BRANCH = 2
HEAVY_CANNON_UPGRADES = [
    ["Модификация 1:\nДобавляются\nбоковые пушки,\nнаносящие меньше урона",
     "Модификация 2:\nБоковые пушки наносят\nв 2 раза больше урона",
     "Сверхмодификация:\nЦентральная пушка\nнаносит в 3 раза\nбольше урона"],
    ["Сильные пушки:\n+3 урона для всех пуль",
     "Сильные пушки:\n+3 урона для всех пуль",
     "Яростные пушки:\n+5 урона для всех пуль",
     "Яростные пушки:\n+5 урона для всех пуль",
     "Несравнимые пушки:\nх1.5 урона для всех пуль"],
    ["Отложенная кара:\n+6 урона для всех пуль,\nперезарядка х1.1",
     "Отложенная кара:\n+6 урона для всех пуль,\nперезарядка х1.1",
     "Мина замедленного\nдействия:\n+10 урона для всех пуль,\nперезарядка х1.1",
     "Мина замедленного\nдействия:\n+10 урона для всех пуль,\nперезарядка х1.1",
     "Неминуемая гибель:\nВы наносите в 2 раза\nбольше урона\nвсеми пушками,\nперезарядка х1.3"]
]


UPGRADES = ["Шанс на выпадение здоровья:",
            "Шанс на выпадение металлолома:",
            "Максимальное здоровье:",
            "Порог опыта для улучшения:"]
UPGRADE_NAMES = ["healthrefillupgradelevel",
                 "scrapchanceupgradelevel",
                 "maxhpupgradelevel",
                 "xprequpgradelevel"]
MAX_UPGRADE_LEVELS = (20, 20, 2, 10)


def calculate_enemies(stage):
    """Рассчитывает врагов, необходимых для перехода на следующий уровень сложности,
    для текущего уровня сложности."""
    return ENEMIES_START + ENEMIES_INCREMENT * (stage - 1)


def calculate_difficulty(stage):
    """Рассчитывает коэффициент сложности для текущего уровня сложности."""
    return DIFFICULTY_START + DIFFICULTY_INCREMENT * (stage - 1)


def calculate_enemy_spawn_timer(stage):
    """Рассчитывает время появления врагов для текущего уровня сложности."""
    return max(ENEMY_SPAWN_TIMER - ENEMY_SPAWN_TIMER_DECREMENT * (stage - 1), 0.5)


def calculate_simultaneous_enemies(stage):
    """Рассчитывает количество врагов, которые могут появляться одновременно, для текущего уровня сложности."""
    return int(SIMULTANEOUS_ENEMIES + SIMULTANEOUS_ENEMIES_INCREMENT * (stage - 1))


def calculate_fighter_chance(stage):
    """Рассчитывает вероятность того, что следующий враг окажется истребителем, для текущего уровня сложности."""
    return FIGHTER_CHANCE + FIGHTER_CHANCE_INCREMENT * (stage % 10 - 1)


def calculate_aircraft_experience(level):
    """Рассчитывает количество опыта, которое нужно для перехода на следующий уровень."""
    upgrades_data = get_upgrades_data()
    return ((EXPERIENCE_TO_LEVEL_UP + EXPERIENCE_INCREMENT * level) *
            (1 - upgrades_data["xprequpgradelevel"] * 0.03))


def calculate_scrap_drop_chance(difficulty):
    """Рассчитывает вероятность получения металлолома с врага."""
    upgrades_data = get_upgrades_data()
    return ((SCRAP_BASE_DROP_CHANCE + SCRAP_DROP_CHANCE_INCREMENT * upgrades_data["scrapchanceupgradelevel"]) *
            difficulty)


def calculate_health_refill_drop_chance():
    """Рассчитывает вероятность получения пополнения здоровья с врага."""
    upgrades_data = get_upgrades_data()
    return HEALTH_BASE_DROP_CHANCE + HEALTH_DROP_CHANCE_INCREMENT * upgrades_data["healthrefillupgradelevel"]


def calculate_aircraft_hp():
    """Рассчитывает максимальное здоровье самолета."""
    upgrades_data = get_upgrades_data()
    return AIRCRAFT_HP + upgrades_data["maxhpupgradelevel"]


def is_boss_stage(stage):
    """Возвращает True, если на уровне сложности присутствует босс."""
    return stage % 10 == 0


def calculate_upgrades_price(upgrade_id, level):
    """Возвращает стоимость определенного уровня определенного улучшения."""
    if upgrade_id == 0 and level <= 20:
        return 10 * level
    elif upgrade_id == 1 and level <= 20:
        return 100 * level
    elif upgrade_id == 2 and level <= 2:
        return 100 * 5 ** level
    elif upgrade_id == 3 and level <= 10:
        return 500 * level
    else:
        return -1
