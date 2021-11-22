import numpy as np
import pygame
import math
import random
from random import randint

from classes import Bacteria, Food

rendering = True

FPS = 600
WIDTH = 1000
HEIGHT = 600

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
BG_COL = [100, 100, 140]
COLORS = [RED, GREEN, BLUE, WHITE]

food_arr = []
bacteria_arr = []
food_spawn_cd = 10
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

    if m_total != 0:
        x_res /= m_total
        y_res /= m_total
    else:
        x_res = x
        y_res = y
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
        if bact.damage != 0:
            r_mass = 1 / bact.damage ** 3
        else:
            r_mass = 0
        r_m_total += r_mass
        r_x_res += bact.x * r_mass
        r_y_res += bact.y * r_mass
        # Green
        if bact.efficiency != 0:
            g_mass = 1 / bact.efficiency ** 3
        else:
            g_mass = 0
        g_m_total += g_mass
        g_x_res += bact.x * g_mass
        g_y_res += bact.y * g_mass
        # Blue
        if bact.defence != 0:
            b_mass = 1 / bact.defence ** 3
        else:
            b_mass = 0
        b_m_total += b_mass
        b_x_res += bact.x * b_mass
        b_y_res += bact.y * b_mass

    if r_m_total != 0:
        r_x_res /= r_m_total
        r_y_res /= r_m_total
    else:
        r_x_res = x
        r_y_res = y

    if g_m_total != 0:
        g_x_res /= g_m_total
        g_y_res /= g_m_total
    else:
        g_x_res = x
        g_y_res = y

    if b_m_total != 0:
        b_x_res /= b_m_total
        b_y_res /= b_m_total
    else:
        b_x_res = x
        b_y_res = y
    return [[r_x_res, r_y_res], [g_x_res, g_y_res], [b_x_res, b_y_res]]


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
finished = False
bacteria_arr.append(Bacteria(screen, WIDTH//2, HEIGHT//2, 10, 0, 0, 1))
main_font = pygame.font.Font(None, 20)

for i in range(100):
    new_food_x = randint(0, WIDTH)
    new_food_y = randint(0, HEIGHT)

    food_arr.append(Food(screen, new_food_x, new_food_y))

while not finished:
    screen.fill(BG_COL)

    clock.tick(FPS)
    fps_text = main_font.render(str(round(clock.get_fps(), 2)), True, [0, 0, 0])
    screen.blit(fps_text, (10, 10))

    if len(food_arr) < 100:
        if food_spawn_cd_current > 0:
            food_spawn_cd_current -= 1
        else:
            food_spawn_cd_current = food_spawn_cd

            new_food_x = randint(0, WIDTH)
            new_food_y = randint(0, HEIGHT)

            food_arr.append(Food(screen, new_food_x, new_food_y))

    for bact in bacteria_arr:
        bact.hunger += 1
        if bact.hunger >= 2000 + 100 * bact.efficiency:
            bacteria_arr.remove(bact)

        food_mc = calculate_food_mass_center(bact.x, bact.y)
        rgb_mc = calculate_bacterias_mass_center(bact.x, bact.y)
        bact.move([food_mc[0] - bact.x, food_mc[1] - bact.y,
                   rgb_mc[0][0] - bact.x, rgb_mc[0][1] - bact.y,
                   rgb_mc[1][0] - bact.x, rgb_mc[1][1] - bact.y,
                   rgb_mc[2][0] - bact.x, rgb_mc[2][1] - bact.y,
                   math.sin(clock.get_rawtime())])

        # Food consumption
        for food in food_arr:
            d = ((bact.x - food.x)**2 + (bact.y - food.y)**2)**0.5
            if d < bact.size + 2:
                bact.hunger -= 600 * bact.efficiency
                food_arr.remove(food)

        # Reproduction
        if bact.hunger < -200:
            bact.hunger = 0

            reproduction_angle = randint(0, 360) / 180 * math.pi
            rep_cos = math.cos(reproduction_angle)
            rep_sin = math.sin(reproduction_angle)

            new_x = bact.x + (2 * bact.size + 5) * rep_cos
            new_y = bact.y + (2 * bact.size + 5) * rep_sin

            new_bact = Bacteria(screen, new_x, new_y, bact.size, bact.damage, bact.defence, bact.efficiency)
            if random.random() < 0.05:
                new_bact.mutate()
            bacteria_arr.append(new_bact)


    # Rendering

    if rendering:
        for food in food_arr:
            food.draw()

        for bact in bacteria_arr:
            bact.draw()

    pygame.display.update()

    # Event handling

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                rendering = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                rendering = True
