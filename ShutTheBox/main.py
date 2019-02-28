#!/usr/local/bin/python3
# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


import sys

sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning')
sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/shut-the-box-env')

sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL')
sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL/ShutTheBox/shut-the-box-env')

import ShutTheBox.agent.Agent as agnt
import ShutTheBox.agent.ReadWrite as rw
import MultiThreadTrain as multiThread


if __name__ == '__main__':
    print('welcome Shut The Box')
    multiThread.train(10)
