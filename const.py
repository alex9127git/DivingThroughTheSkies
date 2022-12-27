"""Класс, в котором хранятся все константы программы, а также функции, вычисляющие значения по формуле."""
import pygame
pygame.font.init()
WIDTH = 800
HEIGHT = 600
MAX_ACCELERATION = 200
COOLDOWN = 1
BULLET_SPEED = 1000
AIRCRAFT_HP = 3
ENEMIES_START = 5
ENEMIES_INCREMENT = 2
SIMULTANEOUS_ENEMIES = 3
SIMULTANEOUS_ENEMIES_INCREMENT = 0.2
DIFFICULTY_START = 1.0
DIFFICULTY_INCREMENT = 0.2
ENEMY_SPAWN_TIMER = 3.0
ENEMY_SPAWN_TIMER_DECREMENT = 0.2
FIGHTER_CHANCE = 20
FIGHTER_CHANCE_INCREMENT = 10
FONT = pygame.font.Font("data/Old-Soviet.otf", 24)


def calculate_enemies(stage):
    """Рассчитывает врагов, необходимых для перехода на следующий уровень сложности,
    для текущего уровня сложности."""
    return ENEMIES_START + ENEMIES_INCREMENT * (stage - 1)


def calculate_difficulty(stage):
    """Рассчитывает коэффициент сложности для текущего уровня сложности."""
    return DIFFICULTY_START + DIFFICULTY_INCREMENT * (stage - 1)


def calculate_enemy_spawn_timer(stage):
    """Рассчитывает время появления врагов для текущего уровня сложности."""
    return max(ENEMY_SPAWN_TIMER - ENEMY_SPAWN_TIMER_DECREMENT * (stage - 1), 0.2)


def calculate_simultaneous_enemies(stage):
    """Рассчитывает количество врагов, которые могут появляться одновременно, для текущего уровня сложности."""
    return int(SIMULTANEOUS_ENEMIES + SIMULTANEOUS_ENEMIES_INCREMENT * (stage - 1))


def calculate_fighter_chance(stage):
    """Рассчитывает вероятность того, что следующий враг окажется истребителем, для текущего уровня сложности."""
    return FIGHTER_CHANCE + FIGHTER_CHANCE_INCREMENT * (stage - 1)
