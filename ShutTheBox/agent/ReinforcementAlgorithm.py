# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import numpy as np
from ShutTheBox.agent import AgentConfiguration as Config
import operator
import random


# https://en.wikipedia.org/wiki/Q-learning
# Our RL algorithm of choice
class QAlgorithm:

    # gets the value of a state V(s)
    @staticmethod
    def value(q, state):
        return max(q[state].items(), key=operator.itemgetter(1))[1]

    # gets the next action according to an epsilon-greedy policy
    @staticmethod
    def next_action(possible_actions, epsilon, is_training=True):
        if np.random.uniform() < epsilon and is_training:
            return random.choice(list(possible_actions))
        else:
            return max(possible_actions.items(), key=operator.itemgetter(1))[0]

    # gets the new q value for a state-action pair Q(s, a)

    def get_new_q_value(self, q, state, action, next_reward, next_state):
        return ((1 - Config.ALPHA) * q[state][action]) + \
               (Config.ALPHA * (next_reward + (Config.GAMMA * QAlgorithm.value(q, next_state))))
