# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
from gym import error, spaces, utils
from gym.utils import seeding


class ShutTheBoxEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        print('inside init')

    def step(self, action):
        pass

    def reset(self):
        pass

    def render(self, mode='human', close=False):
        pass
