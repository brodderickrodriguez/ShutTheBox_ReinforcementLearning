# Brodderick Rodriguez
# Auburn University - CSSE
# 10 Mar. 2019

from ShutTheBox.agent import Agent
from ShutTheBox.agent import AgentConfiguration as agt_config
import matplotlib.pyplot as plt
import numpy as np


GAMMA_VALUES = np.linspace(0.9, 0.99, num=25)
ALPHA_VALUES = [0.02] # np.linspace(0.0019, 0.0023, num=5)
EPOCH_ITERATIONS = 30

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

                agt_config.GAMMA = GAMMA_VALUES[i]
                agt_config.ALPHA = ALPHA_VALUES[j]

                agent = Agent.Agent(print=False)
                win_ratio = agent.learn()
                results[i, j, k] = win_ratio


def make_graph():

    for i in range(len(ALPHA_VALUES)):
        gamma_line = []
        for j in range(len(GAMMA_VALUES)):
            wrs = results[j, i]
            gamma_line.append(np.mean(wrs))

        lbl = str('{0:0.4f}'.format(GAMMA_VALUES[i]))
        plt.plot(gamma_line, label=lbl)

    plt.xticks([i for i in range(len(GAMMA_VALUES))], GAMMA_VALUES)
    plt.ylabel('win ratio')
    plt.xlabel('alpha')
    plt.legend(loc='upper right')
    plt.xticks(rotation='vertical')
    plt.show()


if __name__ == '__main__':
    tune()
    make_graph()
