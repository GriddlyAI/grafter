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

![multi-agent obs](https://github.com/Bam4d/grafter/tree/raw/main/media/initial_obs_global.png)

### PlayerSprite2D

The traditional *crafter* environment observation space, with inventory rendered below the agent's view of the environment:

![player 1 obs](https://github.com/Bam4d/grafter/tree/raw/main/media/initial_obs_player1.png)
![player 2 obs](https://github.com/Bam4d/grafter/tree/raw/main/media/initial_obs_player2.png)
![player 3 obs](https://github.com/Bam4d/grafter/tree/raw/main/media/initial_obs_player3.png)
![player 4 obs](https://github.com/Bam4d/grafter/tree/raw/main/media/initial_obs_player4.png)

### Entity

Provides arrays of entitiy features that can be used with Transformer Models such as Entity Neural Networks.
Examples of training using this observation space can be found here: https://github.com/entity-neural-network/enn-zoo

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

