import gym

from grafter.wrapper import GrafterWrapper
from griddly.RenderTools import VideoRecorder

if __name__ == '__main__':

    env = GrafterWrapper(100, 100)
    env.reset()

    initial_obs = env.render(observer='global', mode='rgb_array')

    global_recorder = VideoRecorder()
    global_recorder.start('global_video.mp4', initial_obs.shape)

    player_recorders = []
    for p in range(env.player_count):
        player_recorder = VideoRecorder()
        initial_obs = env.render(observer=p, mode='rgb_array')
        player_recorder.start(f'player_{p}_video.mp4', initial_obs.shape)

        player_recorders.append(player_recorder)

    # Replace with your own control algorithm!
    for s in range(10000):
        obs, reward, done, info = env.step(env.action_space.sample())

        for p in range(env.player_count):
           env.render(observer=p) # Renders the environment from the perspective of a single player
           frame = env.render(observer=p, mode='rgb_array')
           player_recorders[p].add_frame(frame)

        env.render(observer='global') # Renders the entire environment
        frame = env.render(observer='global', mode='rgb_array')
        global_recorder.add_frame(frame)

        if done:
            env.reset()