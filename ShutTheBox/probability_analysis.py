# Brodderick Rodriguez
# Auburn University - CSSE
# 10 Mar. 2019

from shut_the_box_env.envs import EnvironmentConfiguration
import collections
import numpy as np
import matplotlib.pyplot as plt

env_config = EnvironmentConfiguration.NormalEnvironmentConfiguration()
# env_config = EnvironmentConfiguration.SimpleEnvironmentConfiguration()


def _get_all_possible_rolls():
    if env_config.dice_sum_range == (2, 12):
        # this list comprehension avoids duplicate roles. i.e. (1, 6) = (6, 1) here
        rolls = [[j, i] if j > 0 else [i]
                 for i in range(env_config.dice_range[0], env_config.dice_range[1] + 1)
                 for j in range(env_config.dice_range[0], i + 1)]
    else:
        rolls = [[i] for i in range(env_config.dice_range[0], env_config.dice_range[1] + 1)]

    rolls.sort()
    return rolls


def dice_combos():
    r = range(1, 7)
    # return [(i, j) for i in r for j in r]
    return [i for i in r]


def get_dice_sums(possible_rolls):
    return [np.sum(i) for i in possible_rolls]


def generate_graph_of_roll_sum_probability():
    combos = dice_combos()
    sums = get_dice_sums(combos)
    sum_counts = collections.Counter(sums)
    print(sum_counts)
    exit()
    sums_list = [sum_counts[i] / len(sum_counts) for i in range(2, 13)]

    sums_list = [np.round(s, 3) for s in sums_list]

    print(sums_list)

    plt.bar(np.arange(len(sums_list)), sums_list)
    plt.xticks([i for i in range(len(sums_list))], [i for i in range(2, 13)])
    plt.ylabel('probability')
    plt.xlabel('roll sum')
    plt.show()


if __name__ == '__main__':

    # generate_graph_of_roll_sum_probability()

    s = [1.0/(6**i) for i in range(1, 7)]
    print(sum(s))
