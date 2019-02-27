# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

TILE_RANGE = (1, 12)
DICE_RANGE = (1, 6)
DICE_SUM_RANGE = (2, 12)

class ActionSpace:
    def __init__(self):
        pass

    @staticmethod
    def get_all_possible_rolls():
        rolls = [[j, i] if j > 0 else [i]
                 for i in range(DICE_RANGE[0], DICE_RANGE[1] + 1)
                 for j in range(DICE_RANGE[0], i + 1)]

        rolls.sort()
        return rolls

    def get_all_possible_roll_sums(self):
        rolls = self.get_all_possible_rolls()
        return list(set([sum(roll) for roll in rolls]))

    @staticmethod
    def get_all_possible_tile_combinations():
        combinations = [[j, i] if j != 0 else [i]
                        for i in range(TILE_RANGE[0], TILE_RANGE[1] + 1)
                        for j in range(TILE_RANGE[0] - 1, i + 1)
                        if i + j <= TILE_RANGE[1] and i != j]

        combinations.sort()
        return combinations

    def get_actions_for_roll_sum(self, roll_sum):
        if roll_sum < DICE_SUM_RANGE[0] or roll_sum > DICE_SUM_RANGE[1]:
            raise ValueError('roll sum must be in range [2, 12]')

        actions = [action for action in self.get_all_possible_tile_combinations() if sum(action) == roll_sum]
        return actions





# class ActionSpace:
#     def __init__(self):
#         self.actions = self.get_all_possible_actions()
#
#
#     @staticmethod
#     def get_all_possible_rolls():
#         return [[j, i] if j > 0 else [i] for i in range(1, 6 + 1) for j in range(0, i + 1)]
#
#     def get_all_possible_roll_sums(self):
#         return list(set([sum(l) for l in self.get_all_possible_rolls()]))
#
#     def get_all_possible_actions_for_roll_sum(self, roll_sum):
#         return [l for l in self.get_all_possible_rolls() if sum(l) == roll_sum]
#
#
#
#     @staticmethod
#     def get_all_possible_actions():
#         return [[j, i] for i in range(1, 6 + 1) for j in range(1, i + 1)]
#
#     def get_all_possible_action_sums(self):
#         return list(set([sum(i) for i in self.get_all_possible_actions()]))
#
#     def sample(self, n):
#         possible_actions = self.get_actions_for_roll(n)
#         random_action_index = np.random.randint(0, len(possible_actions))
#         return possible_actions[random_action_index]
#
#     def get_actions_for_roll(self, roll):
#         return [action for action in self.actions if sum(action) == roll]
#
