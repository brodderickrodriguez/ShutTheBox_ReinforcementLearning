# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import numpy as np
from ShutTheBox import Configuration as Config
import operator
import random

# https://en.wikipedia.org/wiki/Q-learning


class QAlgorithm:

    @staticmethod
    def value(q, state):
        return max(q[state].items(), key=operator.itemgetter(1))[1]

    @staticmethod
    def next_action(possible_actions, epsilon, is_training=True):
        if np.random.uniform() < epsilon and is_training:
            return random.choice(list(possible_actions))
        else:
            return max(possible_actions.items(), key=operator.itemgetter(1))[0]

    def get_new_q_value(self, q, state, action, next_reward, next_state):
        return Config.ALPHA * (next_reward + Config.GAMMA * self.value(q=q, state=next_state) - q[state][action])
