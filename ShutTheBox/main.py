#!/usr/local/bin/python3
# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


import sys

sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL')
sys.path.append('/Users/bcr/Dropbox/PROJECTS/CODE/Python/ShutTheBoxRL/ShutTheBox/shut-the-box-env')

import ShutTheBox.agent.Agent as agnt


if __name__ == '__main__':
    print('welcome Shut The Box')
    agent = agnt.Agent()
    agent.learn()
