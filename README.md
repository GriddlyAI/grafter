# Grafter

A griddly accellerated version of the crafter environment 

## Observation Types

Grafter has several observation spaces which can be selected:

### Vector

An `W`x`H`x`C` vector of the state of the environment.

### PlayerSprite2D

The traditional crafter environment observation space:



### Entity

Provides arrays of entitiy features that can be used with Transformer models such as Entity Neural Networks.
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

