import functools

from grafter.level_generators.base import LevelGenerator
import numpy as np
import opensimplex

class CrafterLevelGenerator(LevelGenerator):
    """
    Pretty much this: https://github.com/danijar/crafter/blob/main/crafter/worldgen.py
    """

    def __init__(self, seed, width, height, num_players):
        super().__init__(seed, width, height, num_players, "Crafter")

        self._walkable = {'G', 'P', 'S'}

    def generate(self):
        """
        Generate a crafter-style level and return the griddly level string for it
        :return:
        """
        world = np.chararray(shape=(self._width, self._height), unicode=True, itemsize=5)

        simplex = opensimplex.OpenSimplex(seed=self._random.randint(0, 2 ** 31 - 1))
        for x in range(self._width):
            for y in range(self._height):
                self._set_material(world, (x, y), simplex)
        for x in range(self._width):
            for y in range(self._height):
                self._set_object(world, (x, y))

    def _set_material(self, world, pos, simplex):
        x, y = pos
        start_x, start_y = np.random.randint((0,0),(self._width, self._height))
        simplex = functools.partial(self._simplex, simplex)
        uniform = self._random.uniform
        start = 4 - np.sqrt((x - start_x) ** 2 + (y - start_y) ** 2)
        start += 2 * simplex(x, y, 8, 3)
        start = 1 / (1 + np.exp(-start))
        water = simplex(x, y, 3, {15: 1, 5: 0.15}, False) + 0.1
        water -= 2 * start
        mountain = simplex(x, y, 0, {15: 1, 5: 0.3})
        mountain -= 4 * start + 0.3 * water
        if start > 0.5:
            world[x, y] = 'g'
        elif mountain > 0.15:
            if simplex(x, y, 6, 7) > 0.15 and mountain > 0.3:  # cave
                world[x, y] = 'p'
            elif simplex(2 * x, y / 5, 7, 3) > 0.4:
                world[x, y] = 'p'
                #tunnels[x, y] = True
            elif simplex(x / 5, 2 * y, 7, 3) > 0.4:
                world[x, y] = 'p'
                #tunnels[x, y] = True
            elif simplex(x, y, 1, 8) > 0 and uniform() > 0.85:
                world[x, y] = 'c'
            elif simplex(x, y, 2, 6) > 0.4 and uniform() > 0.75:
                world[x, y] = 'i'
            elif mountain > 0.18 and uniform() > 0.994:
                world[x, y] = 'd'
            elif mountain > 0.3 and simplex(x, y, 6, 5) > 0.35:
                world[x, y] = 'L'
            else:
                world[x, y] = 's'
        elif 0.25 < water <= 0.35 and simplex(x, y, 4, 9) > -0.2:
            world[x, y] = 'S'
        elif 0.3 < water:
            world[x, y] = 'W'
        else:  # grassland
            if simplex(x, y, 5, 7) > 0 and uniform() > 0.8:
                world[x, y] = 't'
            else:
                world[x, y] = 'g'

    def _set_object(self, world, pos, players, tunnels):
        x, y = pos
        uniform = self._random.uniform

        dist = np.inf
        for player_pos in players:
            cur_dist = np.linalg.norm(player_pos - pos)
            if cur_dist < dist:
                dist = dist

        material = world[x, y]
        if material not in self._walkable:
            pass
        elif dist > 3 and material == 'g' and uniform() > 0.985:
            world[x, y] = f'#/{material}'
        elif dist > 10 and uniform() > 0.993:
            world[x, y] = f'!/{material}'
        elif material == 'p' and tunnels[x, y] and uniform() > 0.95:
            world[x, y] = f'@/{material}'

    def _simplex(self, simplex, x, y, z, sizes, normalize=True):
        if not isinstance(sizes, dict):
            sizes = {sizes: 1}
        value = 0
        for size, weight in sizes.items():
            value += weight * simplex.noise3d(x / size, y / size, z)
        if normalize:
            value /= sum(sizes.values())
        return value


