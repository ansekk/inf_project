import numpy as np
import pygame
import math
import random
from random import randint

from classes import Bacteria

rendering = False

FPS = 60
WIDTH = 800
HEIGHT = 600

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
COLORS = [RED, GREEN, BLUE, WHITE]


if rendering:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    bacteria1 = Bacteria(screen)
    bacteria2 = Bacteria(screen)
    finished = False

    while not finished:
        screen.fill(WHITE)
        bacteria1.draw()
        bacteria2.draw()
        pygame.display.update()
