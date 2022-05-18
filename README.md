# Grafter

An accelerated version of the [crafter](https://github.com/danijar/crafter) environment using the [Griddly](https://griddly.readthedocs.io/en/latest/) engine.
This implementation of the crafter environment contains several new features including:

* Hardware accelerated rendering
* Multi-Agent support
* Multiple Observation Spaces

We hope that this version of the crafter environment provides more flexibility for different research approaches!

Join the [Griddly Discord](https://discord.gg/CXpHPrc5Fx) to ask any questions!

## Observation Types

Grafter has several observation spaces which can be selected:

### Vector

An `W`x`H`x`C` vector of the state of the environment.

The vector `C` is a combination of all of the object types and their respective variable values.

Global variables for each player can be retrived using `env.game.get_global_varible([... list of variable names ... ])`

For example to get all the inventory for energy, drink, health and food, you can do:
```
env.game.get_global_variable(["inv_energy", "inv_drink", "inv_health", "inv_food"])
```

A list of all possible variables can be found in the `grafter_base.yaml` GDY file 

### GlobalSprite2D

A global view of the entire environment with players highlighted:

![multi-agent obs](https://github.com/Bam4d/grafter/raw/main/media/initial_obs_global.png)

### PlayerSprite2D

The traditional *crafter* environment observation space, with inventory rendered below the agent's view of the environment:

![player 1 obs](https://github.com/Bam4d/grafter/raw/main/media/initial_obs_player1.png)
![player 2 obs](https://github.com/Bam4d/grafter/raw/main/media/initial_obs_player2.png)
![player 3 obs](https://github.com/Bam4d/grafter/raw/main/media/initial_obs_player3.png)
![player 4 obs](https://github.com/Bam4d/grafter/raw/main/media/initial_obs_player4.png)

### Entity

Provides arrays of entitiy features that can be used with Transformer Models such as Entity Neural Networks.
Examples of training using this observation space can be found here: https://github.com/entity-neural-network/enn-zoo

Using this we can achieve an average (over 10 seeds) "crafter score" of around 15 after 1M steps, which takes approximately 30 minutes of training:

![crafter score](https://github.com/Bam4d/grafter/raw/main/media/crafter_score_entity.png)

> :warning: **Please Note:** *Entity Observations are a simpler challenge to learn than the high level features in the original paper*

## Single Agent Example using CleanRL

To train using either pixels or using vectorized representation of the observation space you can use the following:
```commandline
train/ppo.py --width=30 --height=30 --observer-type=[PlayerSprite2D|Vector]
```


## Using multiple agents

Currently there is no training implementations using multiple agents... by contributions are welcome!

to run multiple agent grafter environments you can use the following snippet:


```python

env = GrafterWrapper(
    height, 
    width, 
    player_count=count, 
    generator_seed=seed, 
    player_observer_type=observer_type, 
    global_observer_type=observer_type
)

```

## Playing as a human

you can create a script with the following to [play as a human](https://github.com/Bam4d/grafter/blob/main/grafter/utils/human_player):

```python
env = GrafterWrapper(30, 30)
env = PlayWrapper(env, seed=100)
env.play(fps=3)
```

## Differences between crafter and grafter

* Balancing of chunks (spawning and despawning NPCs) is not currently possible using Griddly
  * NPCs spawn at the start of the episode and once NPCs are defeated, they are gone from the environment.
* Chasing mechanics in grafter use A* search making the zombies and skeletons more dangerous.
* Probabilities for attacking/chasing in grafter are close the the originals in crafter, but not exactly the same.
* Players can defeat each other, and will gain the opposing player's inventory.

## Additional notes

When using `Entity` or `Vector` observers, the day/night cycle makes very little difference because these observations do not 
