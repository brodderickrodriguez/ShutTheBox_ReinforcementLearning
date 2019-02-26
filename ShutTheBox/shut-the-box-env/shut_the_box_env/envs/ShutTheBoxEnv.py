# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class ActionSpace:
    def __init__(self):
        self.actions = self.get_all_possible_actions()

    @staticmethod
    def get_all_possible_actions():
        actions = []
        for n in range(1, 12 + 1):
            actions.append([[i, n - i] if i != n else [n] for i in range(1, n + 1)])
        return actions

    def sample(self, n):
        possible_actions = self.get_actions_for_roll(n)
        random_action_index = np.random.randint(0, len(possible_actions))
        return possible_actions[random_action_index]

    def get_actions_for_roll(self, n):
        return self.actions[n - 1]


class ShutTheBoxEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = ActionSpace()
        self.tiles = self._generate_clean_tiles()

    @staticmethod
    def roll_dice_get_sum():
        die1 = np.random.randint(1, 6 + 1)
        die2 = np.random.randint(1, 6 + 1)
        return die1 + die2

    def roll_and_get_possible_actions(self):
        s = self.roll_dice_get_sum()
        return self.action_space.get_actions_for_roll(s)

    def hash_tiles_and_roll_to_string(self, roll):
        s = ''
        for tile in self.tiles:
            s += str(tile)
        return s + str(roll)

    def step(self, action):
        if type(action) != list:
            raise TypeError('action is not a list')

        for tile_index in list(action):
            self.tiles[tile_index - 1] = 0

        # not sure if there is a bug here or not
        # done is based off of next roll by design
        # could cause problems
        # usual gym implementation this isn't the case
        # game over might need to happen after that action is taken
        next_roll = self.roll_dice_get_sum()
        done = self.check_game_over(next_roll)
        reward = self.get_reward_for_current_state(done)
        observation_string = self.hash_tiles_and_roll_to_string(next_roll)

        return observation_string, reward, done, {}

    def get_reward_for_current_state(self, game_over):
        if sum(self.tiles) == 0:
            return 10
        if game_over:
            return -10
        return -0.1

    def check_game_over(self, next_roll):
        possible_next_actions = self.action_space.get_actions_for_roll(next_roll)

        for action_pair in possible_next_actions:
            tiles_up = [self.tiles[action_tile - 1] for action_tile in action_pair]

            if sum(tiles_up) == len(action_pair):
                return False

        return True

    @staticmethod
    def _generate_clean_tiles():
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def reset(self):
        self.tiles = self._generate_clean_tiles()

    def render(self, mode='human', close=False):
        pass
