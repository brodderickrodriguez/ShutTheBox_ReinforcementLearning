# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import random


class ActionSpace:
    def __init__(self):
        self.tile_range = (1, 12)
        self.dice_range = (1, 6)
        self.dice_sum_range = (2, 12)

    def _get_all_possible_rolls(self):
        rolls = [[j, i] if j > 0 else [i]
                 for i in range(self.dice_range[0], self.dice_range[1] + 1)
                 for j in range(self.dice_range[0], i + 1)]

        rolls.sort()
        return rolls

    def get_all_possible_roll_sums(self):
        rolls = self._get_all_possible_rolls()
        return list(set([sum(roll) for roll in rolls]))

    def get_all_possible_tile_combinations(self):
        combinations = [[j, i] if j != 0 else [i]
                        for i in range(self.tile_range[0], self.tile_range[1] + 1)
                        for j in range(self.tile_range[0] - 1, i + 1)
                        if i + j <= self.tile_range[1] and i != j]

        combinations.sort()
        return combinations

    def get_actions_for_roll_sum(self, roll_sum):
        if roll_sum < self.dice_sum_range[0] or roll_sum > self.dice_sum_range[1]:
            raise ValueError('roll sum must be in range [2, 12]')

        return [action for action in self.get_all_possible_tile_combinations() if sum(action) == roll_sum]

    def sample_action_from_roll_sum(self, roll_sum):
        actions = self.get_actions_for_roll_sum(roll_sum=roll_sum)
        random_action_index = random.randint(0, len(actions) - 1)
        return actions[random_action_index]
