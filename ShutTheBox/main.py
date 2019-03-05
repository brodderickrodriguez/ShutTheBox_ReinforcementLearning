#!/usr/local/bin/python3
# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


import sys
import ShutTheBox.MultiProcessTrain as mpt


def handle_relative_imports():
    # for hopper cluster
    sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning')
    sys.path.append('/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/shut-the-box-env')

    # for bcr local
    sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL')
    sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL/ShutTheBox/shut-the-box-env')


if __name__ == '__main__':
    print('welcome Shut The Box')
    handle_relative_imports()

    # 100,000
    train_iterations = int(5)
    processes = 2

    train = mpt.MultiProcessTrain()
    train.train_agents(processes_count=processes, iterations=train_iterations)

    # each agent plays 10,000 games in one epoch
    # multiplied by the number of train iterations
    # multiplied by the number of processes
