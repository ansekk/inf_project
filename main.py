import numpy as np
import pygame
import math
import random
from random import randint

from classes import Bacteria, Food

rendering = True

FPS = 60
WIDTH = 800
HEIGHT = 600

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
BG_COL = [100, 100, 140]
COLORS = [RED, GREEN, BLUE, WHITE]

food_arr = []
bacteria_arr = []
food_spawn_cd = 20
food_spawn_cd_current = 0
mouse_pos = [0, 0]


def calculate_food_mass_center(x, y):
    x_res = 0
    y_res = 0
    m_total = 0

    for food in food_arr:
        r = max(((x - food.x)**2 + (y - food.y)**2)**0.5, 1)
        mass = 1 / r ** 3
        m_total += mass
        x_res += food.x * mass
        y_res += food.y * mass

    x_res /= m_total
    y_res /= m_total
    return [x_res, y_res]


def calculate_bacterias_mass_center(x, y):
    # Red
    r_x_res = 0
    r_y_res = 0
    r_m_total = 0
    # Green
    g_x_res = 0
    g_y_res = 0
    g_m_total = 0
    # Blue
    b_x_res = 0
    b_y_res = 0
    b_m_total = 0

    for bact in bacteria_arr:
        r = max(((x - bact.x) ** 2 + (y - bact.y) ** 2) ** 0.5, 1)
        # Red
        r_mass = 1 / bact.damage ** 3
        r_m_total += r_mass
        r_x_res += bact.x * r_mass
        r_y_res += bact.y * r_mass
        # Green
        g_mass = 1 / bact.efficiency ** 3
        g_m_total += g_mass
        g_x_res += bact.x * g_mass
        g_y_res += bact.y * g_mass
        # Blue
        b_mass = 1 / bact.defence ** 3
        b_m_total += b_mass
        b_x_res += bact.x * b_mass
        b_y_res += bact.y * b_mass

    r_x_res /= r_m_total
    r_y_res /= r_m_total
    g_x_res /= g_m_total
    g_y_res /= g_m_total
    b_x_res /= b_m_total
    b_y_res /= b_m_total
    return [[r_x_res, r_y_res], [g_x_res, g_y_res], [b_x_res, b_y_res]]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False
bacteria_arr.append(Bacteria(screen, WIDTH//2, HEIGHT//2, 10, 0, 0, 1))


while not finished:
    clock.tick(FPS)

    if len(food_arr) < 50:
        if food_spawn_cd_current > 0:
            food_spawn_cd_current -= 1
        else:
            food_spawn_cd_current = food_spawn_cd

        new_food_x = randint(0, WIDTH)
        new_food_y = randint(0, HEIGHT)

        food_arr.append(Food(screen, new_food_x, new_food_y))

    # Rendering

    if rendering:
        screen.fill(BG_COL)

        for food in food_arr:
            food.draw()

        for bact in bacteria_arr:
            bact.draw()

        mc_test = calculate_food_mass_center(mouse_pos[0], mouse_pos[1])

        pygame.draw.circle(screen, RED, (mc_test[0], mc_test[1]), 2)

        pygame.display.update()

    # Event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
