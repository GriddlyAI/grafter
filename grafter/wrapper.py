from pathlib import Path

import gym
from griddly import GymWrapper, gd

from grafter.level_generators.crafter_generator import CrafterLevelGenerator


class GrafterWrapper(gym.Env):

    def __init__(self, width, height, seed=100, player_observer_type=gd.ObserverType.VECTOR, global_observer_type=gd.ObserverType.SPRITE_2D):

        current_file = Path(__file__).parent
        self._genv = GymWrapper(
            yaml_file='grafter_base.yaml',
            global_observer_type=global_observer_type,
            player_observer_type=player_observer_type,
            max_steps=None,
            gdy_path=str(current_file.joinpath('gdy')),
            image_path=str(current_file.joinpath('assets')),
        )

        self._generator = CrafterLevelGenerator(seed, width, height, 1)

    def step(self, action):
        return self._genv.step(action)

    def reset(self):
        level_string = self._generator.generate()
        self._genv.reset(level_string=level_string)

    def render(self, mode="human"):
        pass
