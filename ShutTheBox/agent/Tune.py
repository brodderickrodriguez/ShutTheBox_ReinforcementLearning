# Brodderick Rodriguez
# Auburn University - CSSE
# 10 Mar. 2019

from ShutTheBox.agent import Agent
from ShutTheBox.agent import AgentConfiguration
import matplotlib.pyplot as plt
import numpy as np


GAMMA_VALUES = np.linspace(0.9, 0.99, num=5)
ALPHA_VALUES = np.linspace(0.001, 0.1, num=5)
EPOCH_ITERATIONS = 5

# dim0: gamma value
# dim1: alpha value
# dim2: epoch values
results = np.zeros((len(GAMMA_VALUES), len(ALPHA_VALUES), EPOCH_ITERATIONS))
print(results.shape)


def tune():
    print('tuning...')

    for i in range(len(GAMMA_VALUES)):
        for j in range(len(ALPHA_VALUES)):
            for k in range(EPOCH_ITERATIONS):
                print(k)

                agent = Agent.Agent()
                win_ratio = agent.learn()

                results[i][j][k] = win_ratio


def make_graph():
    pass




if __name__ == '__main__':
    tune()
    make_graph()
