# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
import shut_the_box_env
import numpy as np



def perform():
    env = gym.make('shut_the_box_env-v0')
    env.reset()

    initial_roll_sum = env.roll_dice_get_sum()
    initial_action = env.action_space.sample(initial_roll_sum)


    observation, reward, done, info = env.step(initial_action)

    # while not done:



def main():
    print('welcome Shut The Box')
    perform()


if __name__ == '__main__':
    main()