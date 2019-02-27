# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
import numpy as np
import shut_the_box_env.envs


class ShutTheBoxEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.action_space = shut_the_box_env.envs.ActionSpace.ActionSpace()
        self.tiles = self._generate_clean_tiles()

    @staticmethod
    def roll_dice_get_sum():
        die1 = np.random.randint(1, 6 + 1)
        die2 = np.random.randint(1, 6 + 1)
        return die1 + die2

    def hash_tiles_and_roll_to_string(self, roll):
        return ''.join([str(tile) for tile in self.tiles]) + str(roll).zfill(2)

    def step(self, action):
        if type(action) != list:
            raise TypeError('action is not a list')

        for tile_index in list(action):
            if self.tiles[tile_index - 1] == 0:
                raise ValueError('tile {tile} is already down'.format(tile=tile_index))

            self.tiles[tile_index - 1] = 0

        next_roll = self.roll_dice_get_sum()
        observation_string = self.hash_tiles_and_roll_to_string(next_roll)
        done = self.check_game_over(next_roll)
        reward = self.get_reward_for_current_state(done)
        won = 1 if sum(self.tiles) == 0 else 0

        # return tuple: (observation: string, reward: double, done: boolean, info: dict)
        return observation_string, reward, done, {'next_roll': next_roll, 'win': won}

    def get_reward_for_current_state(self, game_over):
        if sum(self.tiles) == 0:
            return 10
        if game_over:
            return -10
        return -0.1

    def check_game_over(self, next_roll):
        return len(self.get_possible_actions_for_roll(next_roll)) == 0

    def get_possible_actions_for_roll(self, roll_sum):
        all_possible_actions = self.action_space.get_actions_for_roll_sum(roll_sum=roll_sum)
        possible_actions = []

        for action in all_possible_actions:
            tile_down = False
            for tile in action:
                if self.tiles[tile - 1] == 0:
                    tile_down = True
                    break

            if not tile_down:
                possible_actions.append(action)

        return possible_actions

    @staticmethod
    def _generate_clean_tiles():
        return [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    def reset(self):
        self.tiles = self._generate_clean_tiles()
        return self.hash_tiles_and_roll_to_string(0)

    def render(self, mode='human', close=False):
        pass
