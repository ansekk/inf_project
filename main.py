import pygame
import math
from random import randint

FPS = 60
WIDTH = 600
HEIGHT = 700

RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
COLORS = [RED, GREEN, BLUE, WHITE]


class Bacteria:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.size = 20
        self.defence = 1
        self.damage = 1
        self.food = 1
        self.color = GREEN
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)
        self.vx = 0
        self.vy = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)

    def move(self):
        if self.x >= WIDTH - self.size:
            self.vx = -self.vx
            self.x = WIDTH - self.size - 1
        if self.y >= HEIGHT - self.size:
            self.y = HEIGHT - self.size - 1
        self.vy = self.vy - 1
        self.x += self.vx
        self.y -= self.vy


class Food:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.size = 2
        self.color = GREEN
        self.x = randint(0, WIDTH)
        self.y = randint(0, HEIGHT)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)


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
