import numpy as np
import random


def create_nn(layers):
    weights = []
    biases = []

    for i in range(len(layers) - 1):
        weights.append(2 * (np.random.sample((layers[i + 1], layers[i])) - 0.5))
        biases.append(2 * (np.random.sample(layers[i + 1]) - 0.5))

    return [weights, biases]


print(random.randint(-1, 0))
