import numpy as np
import pygame
import random
from random import randint


RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]


def __neuron_activation(x):
    return 1 / (1 + np.exp(-x))


def create_nn(layers):
    weights = []
    biases = []

    for i in range(len(layers) - 1):
        weights.append(np.random.sample((layers[i + 1], layers[i])))
        biases.append(np.random.sample(layers[i + 1]))

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
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.sc_w = screen.get_width()
        self.sc_h = screen.get_height()
        self.size = 20
        self.defence = 1
        self.damage = 1
        self.food = 1
        self.color = GREEN
        self.x = randint(0, self.sc_w)
        self.y = randint(0, self.sc_h)
        self.vx = 0
        self.vy = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)

    def move(self):
        if self.x >= self.sc_w - self.size:
            self.vx = -self.vx
            self.x = self.sc_w - self.size - 1
        if self.y >= self.sc_h - self.size:
            self.y = self.sc_h - self.size - 1
        self.vy = self.vy - 1
        self.x += self.vx
        self.y -= self.vy


class Food:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.size = 2
        self.color = GREEN
        self.x = randint(0, self.sc_w)
        self.y = randint(0, self.sc_h)

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.size)


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

