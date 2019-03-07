# Brodderick Rodriguez
# Auburn University - CSSE
# 05 Mar. 2019

import sys
from ShutTheBox.agent import ReinforcementAlgorithm
from ShutTheBox.agent import ReadWrite
from ShutTheBox.agent import AgentConfiguration


class AgentManager:
    def __init__(self):
        # learning rate
        self.ALPHA = 0.01

        # discount factor
        self.GAMMA = 0.90

        # learning algorithm
        self.ra = ReinforcementAlgorithm.QAlgorithm()

        # path to saved model
        # self.q_table_path = Configuration.get_q_table_path()
        # print(self.q_table_path)

    def update_q_table(self, new_q_table):
        pass



