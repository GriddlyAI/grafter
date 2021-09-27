from pathlib import Path

import gym
from griddly import GymWrapper, gd


class GrafterWrapper(gym.Env):

    def __init__(self, player_observer_type=gd.ObserverType.VECTOR, global_observer_type=gd.ObserverType.SPRITE_2D):

        current_file = Path(__file__)
        self._genv = GymWrapper(
            yaml_file='grafter_base.yaml',
            global_observer_type=global_observer_type,
            player_observer_type=player_observer_type,
            max_steps=None,
            gdy_path=current_file.joinpath('gdy').name,
            image_path=current_file.joinpath('assets').name,
        )

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode="human"):
        pass
