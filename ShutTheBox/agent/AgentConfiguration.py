# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import sys
from enum import Enum
from ShutTheBox.agent import ReinforcementAlgorithm
from ShutTheBox.agent import ReadWrite
from ShutTheBox.agent import AgentManager

# learning rate
ALPHA = 0.01

# discount factor
GAMMA = 0.90

# initialize our RL algorithm of choice
ra = ReinforcementAlgorithm.QAlgorithm()

rw = ReadWrite.ReadWrite()

manager = AgentManager.AgentManager()


def add_relative_directory_paths():
    if BuildConfiguration.get_configuration() == BuildConfiguration.LOCAL:
        sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL')
        sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL/ShutTheBox/shut-the-box-env')
    else:
        sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning')
        sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/shut-the-box-env')


def get_q_table_path():
    paths = {
        BuildConfiguration.LOCAL: './agent/models/model.json',
        BuildConfiguration.HOPPER: '/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/agent/models/model.json'}
    return paths[BuildConfiguration.get_configuration()]


class BuildConfiguration(Enum):
    LOCAL = 'local'
    HOPPER = 'hopper'

    @staticmethod
    def get_configuration():
        if BuildConfiguration(sys.argv[1]) is BuildConfiguration.LOCAL:
            return BuildConfiguration.LOCAL
        else:
            return BuildConfiguration.HOPPER

