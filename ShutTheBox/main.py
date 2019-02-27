# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


import ShutTheBox.Agent as agnt

import shut_the_box_env.envs.ActionSpace as act



def main():
    print('welcome Shut The Box')
    agent = agnt.Agent()
    agent.learn()


if __name__ == '__main__':
    main()
