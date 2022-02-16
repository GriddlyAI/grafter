from timeit import default_timer as timer
from grafter.wrapper import GrafterWrapper

if __name__ == '__main__':

    env = GrafterWrapper(200, 200)
    env.reset()
    start = timer()
    frames = 0

    # Replace with your own control algorithm!
    for s in range(20000):
        obs, reward, done, info = env.step(env.action_space.sample())

        #for p in range(env.player_count):
        #    env.render(observer=p) # Renders the environment from the perspective of a single player

        #env.render(observer='global') # Renders the entire environment

        frames += 1

        if frames % 1000 == 0:
            end = timer()
            fps = (frames / (end - start))
            print(f'fps: {fps}')
            frames = 0
            start = timer()

        if done:
            env.reset()