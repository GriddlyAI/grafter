import timeit
import sys
import os

module_path = os.path.dirname(os.path.realpath(__file__))
grafter_path = os.path.join(module_path, "../../../")

sys.path.extend([grafter_path])
from grafter.wrapper import GrafterWrapper

if __name__ == "__main__":

    env = GrafterWrapper(100, 100, level_id=0)

    env.reset()

    start = timeit.default_timer()

    frames = 0

    for i in range(20000):

        obs, reward, done, info = env.step(env.action_space.sample())

        frames += 1

        # env.render()
        # env.render(observer='global')

        if done or i % 1000 == 0:
            end = timeit.default_timer()
            print(f"{len(obs)*frames / (end - start):.2f} SPS")
            frames = 0
            env.reset()
            start = timeit.default_timer()

    print("end")
