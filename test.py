import gym

from grafter.wrapper import GrafterWrapper

if __name__ == '__main__':

    env = GrafterWrapper(100, 100)
    env.reset()

    # Replace with your own control algorithm!
    for s in range(10000):
        obs, reward, done, info = env.step(env.action_space.sample())

        #for p in range(env.player_count):
        #    env.render(observer=p) # Renders the environment from the perspective of a single player

        env.render(observer='global') # Renders the entire environment

        if done:
            env.reset()