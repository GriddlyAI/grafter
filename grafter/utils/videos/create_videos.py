import gym

from grafter.wrapper import GrafterWrapper
from griddly.RenderTools import VideoRecorder,RenderToFile

if __name__ == "__main__":

    env = GrafterWrapper(30, 30, player_count=4)
    env.reset()

    initial_obs = env.render(observer="global", mode="rgb_array")

    render_to_file = RenderToFile()

    render_to_file.render(initial_obs, "images/initial_obs_global.png")
    render_to_file.render(env.render(observer=0, mode="rgb_array"), "images/initial_obs_player1.png")
    render_to_file.render(env.render(observer=1, mode="rgb_array"), "images/initial_obs_player2.png")
    render_to_file.render(env.render(observer=2, mode="rgb_array"), "images/initial_obs_player3.png")
    render_to_file.render(env.render(observer=3, mode="rgb_array"), "images/initial_obs_player4.png")

    global_recorder = VideoRecorder()
    global_recorder.start("videos/global_video.mp4", initial_obs.shape)

    player_recorders = []
    for p in range(env.player_count):
        player_recorder = VideoRecorder()
        initial_obs = env.render(observer=p, mode="rgb_array")
        player_recorder.start(f"videos/player_{p}_video.mp4", initial_obs.shape)

        player_recorders.append(player_recorder)

    # Replace with your own control algorithm!
    for s in range(500):
        obs, reward, done, info = env.step(env.action_space.sample())

        for p in range(env.player_count):
            env.render(
                observer=p
            )  # Renders the environment from the perspective of a single player
            frame = env.render(observer=p, mode="rgb_array")
            player_recorders[p].add_frame(frame)

        env.render(observer="global")  # Renders the entire environment
        frame = env.render(observer="global", mode="rgb_array")
        global_recorder.add_frame(frame)

        if done:
            env.reset()
