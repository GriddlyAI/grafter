from pathlib import Path

import gym
from griddly import GymWrapper, gd

from grafter.level_generators.crafter_generator import CrafterLevelGenerator


class GrafterWrapper(gym.Wrapper):

    def __init__(self, width, height, generator_seed=100, player_observer_type=gd.ObserverType.SPRITE_2D, global_observer_type=gd.ObserverType.SPRITE_2D):

        current_file = Path(__file__).parent
        self._genv = GymWrapper(
            yaml_file='grafter_base.yaml',
            global_observer_type=global_observer_type,
            player_observer_type=player_observer_type,
            max_steps=None,
            gdy_path=str(current_file.joinpath('gdy')),
            shader_path=str(current_file.joinpath('assets/shaders')),
            image_path=str(current_file.joinpath('assets')),
        )

        self._generator = CrafterLevelGenerator(generator_seed, width, height, self._genv.player_count)

        super().__init__(self._genv)

    def step(self, action):
        return self.env.step(action)

    def reset(self):
        level_string = self._generator.generate()
        reset_obs = self.env.reset(level_string=level_string)
        self.action_space = self.env.action_space
        self.observation_space = self.env.action_space

        return reset_obs

    def render(self, mode='human', observer=0):
        return self.env.render(mode=mode, observer=observer)
