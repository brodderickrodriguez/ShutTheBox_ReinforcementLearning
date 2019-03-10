# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
import numpy as np
from .ActionSpace import ActionSpace
from .EnvironmentConfiguration import env_config


# The Shut The Box Environment
class ShutTheBoxEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = ActionSpace()
        self.tiles = self._generate_clean_tiles()

    # roll two dice and return their sum
    @staticmethod
    def roll_dice_get_sum():
        s = sum([np.random.randint(env_config.dice_range[0], env_config.dice_range[1] + 1)
                 for _ in range(env_config.number_of_dice)])
        return s

    # generates a string 'bbbbbbbbbbbbdd', b is binary bit, d is roll sum
    # to hash the current environment state to a string
    def hash_tiles_and_roll_to_string(self, roll):
        return ''.join([str(tile) for tile in self.tiles]) + str(roll).zfill(2)

    # step executes a state and observes the new environment state
    def step(self, action):
        # if input is not a list, raise error and exit
        if type(action) != list:
            raise TypeError('action is not a list')

        # for each tile in the commited action, set its binary bit to zero in the self.tiles list
        for tile_index in list(action):
            # if the tile is already down, raise error and exit
            if self.tiles[tile_index - 1] == 0:
                raise ValueError('tile {tile} is already down'.format(tile=tile_index))

            # set the tile to 0 / off / already played
            self.tiles[tile_index - 1] = 0

        # get our next stochastic dice roll sum
        next_roll = self.roll_dice_get_sum()

        # generate an environment state string based on tiles and roll sum
        observation_string = self.hash_tiles_and_roll_to_string(next_roll)

        # check if game is over and save it in the 'done' flag
        done = self.check_game_over(next_roll)

        # compute a reward for arriving to the current state state
        reward = self.get_reward_for_current_state(done)

        # check if we have won, if we have, set flag to 1, if not set flag to 0
        won = 1 if sum(self.tiles) == 0 else 0

        # return tuple: (observation: string, reward: double, done: boolean, info: dict)
        return observation_string, reward, done, {'next_roll': next_roll, 'win': won}

    # a naive way of computing the reward
    # TODO: use inverse RL to learn a better reward function
    def get_reward_for_current_state(self, game_over):
        # if all tiles are down, we win and want a high reward
        if sum(self.tiles) == 0:
            return 10

        # if we lose, we want a low reward
        if game_over:
            return -5

        # otherwise, penalize the agent for taking another action
        return -0.1

    # returns a boolean: 1 of there are no remaining actions, 0 otherwise
    def check_game_over(self, next_roll):
        return len(self.get_possible_actions_for_roll(next_roll)) == 0

    # gets all possible actions given our current state accounting for tiles remaining and our roll sum
    def get_possible_actions_for_roll(self, roll_sum):
        # returns an exhaustive list of all actions we can take given a roll sum
        all_possible_actions = self.action_space.get_actions_for_roll_sum(roll_sum=roll_sum)
        possible_actions = []

        # for each possible action, check if it is a valid action
        # i.e. one of the tiles in that action is not down
        for action in all_possible_actions:
            # boolean flag to check track if either tiles in the action are down
            tile_down = False
            for tile in action:
                # if one of the tiles is down, set the tile_down flag to true and break the inner loop
                if self.tiles[tile - 1] == 0:
                    tile_down = True
                    break

            # if the tile_down flag is not set, then it is a valid move so we save it
            if not tile_down:
                possible_actions.append(action)

        # return a list of possible actions given tiles remaining and our roll sum
        return possible_actions

    # a reset tile list contains all ones symbolizing each tile is still in the game
    @staticmethod
    def _generate_clean_tiles():
        return [1 for _ in range(env_config.tile_range[1])]

    # resets the tiles and returns the initial state string: '11111111111100'
    def reset(self):
        self.tiles = self._generate_clean_tiles()
        return self.hash_tiles_and_roll_to_string(0)

    # a method from the parent Gym Environment class used to render a GUI for the environment
    def render(self, mode='human', close=False):
        pass
