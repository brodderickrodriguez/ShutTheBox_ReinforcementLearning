# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import random
from .EnvironmentConfiguration import env_config


# A class which helps us maintain our action space given states or roll sums
class ActionSpace:
    def __init__(self):
        # the ranges for tiles in Shut The Box, the possible values of dice, and all possible roll sums given two dice
        self.tile_range = env_config.tile_range
        self.dice_range = env_config.dice_range
        self.dice_sum_range = env_config.dice_sum_range

    # generates all possible rolls of two dice
    def _get_all_possible_rolls(self):
        # this list comprehension avoids duplicate roles. i.e. (1, 6) = (6, 1) here
        rolls = [[j, i] if j > 0 else [i]
                 for i in range(self.dice_range[0], self.dice_range[1] + 1)
                 for j in range(self.dice_range[0], i + 1)]

        rolls.sort()
        return rolls

    # generates a unique-item list of all possible roll sums given any roll of two dice
    def get_all_possible_roll_sums(self):
        rolls = self._get_all_possible_rolls()
        return list(set([sum(roll) for roll in rolls]))

    # computes all possible combinations of moves. The agent can put one or two tiles down at a time
    def get_all_possible_tile_combinations(self):
        combinations = [[j, i] if j != 0 else [i]
                        for i in range(self.tile_range[0], self.tile_range[1] + 1)
                        for j in range(self.tile_range[0] - 1, i + 1)
                        if i + j <= self.tile_range[1] and i != j]

        combinations.sort()
        return combinations

    # computes the possible actions we can take given a roll sum
    def get_actions_for_roll_sum(self, roll_sum):
        if roll_sum < self.dice_sum_range[0] or roll_sum > self.dice_sum_range[1]:
            print(self.dice_sum_range, roll_sum)
            raise ValueError('roll sum must be in range [2, 12]')

        return [action for action in self.get_all_possible_tile_combinations() if sum(action) == roll_sum]

    # returns a random action to take given a roll sum. Used to perform the initial action
    def sample_action_from_roll_sum(self, roll_sum):
        actions = self.get_actions_for_roll_sum(roll_sum=roll_sum)
        random_action_index = random.randint(0, len(actions) - 1)
        return actions[random_action_index]
