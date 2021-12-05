import numpy as np
import pygame
import random
from random import randint


RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
FOOD_COL = [200, 200, 100]


def __neuron_activation(x):
    return 1 / (1 + np.exp(-x))


def create_nn(layers):
    weights = []
    biases = []

    for i in range(len(layers) - 1):
        weights.append(2 * (np.random.sample((layers[i + 1], layers[i])) - 0.5))
        biases.append((np.random.sample(layers[i + 1]) - 0.5))

    return [weights, biases]


def matrix_feed_forward_calc(x, w, b):
    for i in range(len(w)):
        if i == 0:
            node_in = x
        else:
            node_in = h
        z = w[i].dot(node_in) + b[i]
        h = __neuron_activation(z)
    return h


class Bacteria:
    def __init__(self, screen: pygame.Surface, x, y, size, dmg, defence, eff):
        self.screen = screen
        self.sc_w = screen.get_width()
        self.sc_h = screen.get_height()
        self.size = size
        self.defence = defence
        self.damage = dmg
        self.efficiency = eff
        self.hunger = 0
        self.nn = BacteriaNN([9, 5, 2])

        max_stat = max(self.damage, self.efficiency, self.defence)
        self.color = [int(self.damage / max_stat * 255), int(self.efficiency / max_stat * 255), int(self.defence / max_stat * 255)]
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.sc_h - self.y), self.size)

    def move(self, inp_info):
        decision = self.nn.think(inp_info)
        self.vx = (4 * (decision[0] - 0.5))
        self.vy = (4 * (decision[1] - 0.5))
        self.x += self.vx
        self.y += self.vy
        if self.x > self.sc_w:
            self.x -= self.sc_w
        if self.x < 0:
            self.x += self.sc_w
        if self.y > self.sc_h:
            self.y -= self.sc_h
        if self.y < 0:
            self.y += self.sc_h

    def mutate(self):
        if random.random() < 0.5:
            self.size += 2 * random.randint(-1, 1)
            if self.size < 0:
                self.size = -self.size
        if random.random() < 0.5:
            self.damage += random.randint(-1, 1)
            if self.damage < 0:
                self.damage = -self.damage
        if random.random() < 0.5:
            self.defence += random.randint(-1, 1)
            if self.defence < 0:
                self.defence = -self.defence
        if random.random() < 0.5:
            self.efficiency += random.randint(-1, 1)
            if self.efficiency < 0:
                self.efficiency = -self.efficiency
        self.nn.mutate()


class Food:
    def __init__(self, screen: pygame.Surface, x, y):
        self.screen = screen
        self.color = FOOD_COL
        self.sc_w = screen.get_width()
        self.sc_h = screen.get_height()
        self.x = x
        self.y = y

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.sc_h - self.y), 2)


class BacteriaNN:
    def __init__(self, layers):
        nn = create_nn(layers)
        self.w = nn[0]
        self.b = nn[1]

    def think(self, inp):
        return matrix_feed_forward_calc(inp, self.w, self.b)

    def mutate(self):
        for layer in range(len(self.w)):
            for i in range(len(self.w[layer])):
                for j in range(len(self.w[layer][i])):
                    if random.random() < 0.2:
                        self.w[layer][i][j] += (random.random() - 0.5) * 2

                if random.random() < 0.2:
                    self.b[layer][i] += (random.random() - 0.5) * 2

