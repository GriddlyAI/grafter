import numpy as np


class LevelGenerator:
    def __init__(self, seed, height, width, num_players, name):
        self._name = name
        self._height = height
        self._width = width
        self._num_players = num_players
        self._random = np.random.RandomState(seed)

    def generate(self):
        raise NotImplementedError
