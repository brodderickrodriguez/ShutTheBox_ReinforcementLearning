# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import gym
import numpy as np
import itertools
from ShutTheBox import Configuration as Config


class Agent:
    def __init__(self):
        self.env = gym.make('shut_the_box_env-v0')
        print('building q table')
        self.q_table = self.build_q_table()
        print('learning...')
        self.learn()

    def run_single_episode(self, episode_number, epsilon):
        state = self.env.reset()
        actions_taken = []
        done, step_count, total_reward = False, 0, 0
        roll_sum = self.env.roll_dice_get_sum()
        action = self.env.action_space.sample_action_from_roll_sum(roll_sum=roll_sum)

        while not done:
            actions_taken.append(action)
            next_state, reward, done, info = self.env.step(action=action)
            roll_sum = info['next_roll']
            step_count += 1
            total_reward += reward

            if done:
                break

            possible_actions = self.get_possible_next_actions(next_state=next_state, roll_sum=roll_sum)

            next_action = Config.ra.next_action(possible_actions=possible_actions, epsilon=epsilon)

            temp_action = self.action_list_to_string(action)

            self.q_table[state][temp_action] = Config.ra.get_new_q_value(q=self.q_table, state=state,
                                                                         action=temp_action, next_reward=reward,
                                                                         next_state=next_state, next_action=next_action)

            state = next_state
            action = self.string_to_action_list(next_action)


        win = 1 if sum(self.env.tiles) == 0 else 0

        print_string = 'episode {i}:\n\t''actions:\t{a}\n\tstep_count:\t{sc}\n\ttiles:\t{et}\n\tlast_roll:\t{lr}\n\ttotal_reward:\t{tr}'.format(i=episode_number, a=actions_taken, sc=step_count, tr=total_reward, et=self.env.tiles, lr=roll_sum)


        return total_reward, print_string, win



    def learn(self):
        episode = 0
        best_episode = None
        best_reward = float("-infinity")
        wins = 0
        win_ratio_list = []
        epoch_length = 10000

        while True:
            episode += 1
            epsilon = 2 / np.sqrt(np.sqrt(episode + 1))
            reward, print_string, win = self.run_single_episode(episode_number=episode, epsilon=epsilon)

            print(win)

            wins += win

            win_ratio_list.append(win)

            if reward >= best_reward:
                best_episode = print_string
                best_reward = reward

            if episode % epoch_length == 0:
                win_ratio_list = win_ratio_list[epoch_length:]
                win_ratio = sum(win_ratio_list) / epoch_length
                epoch_number = int(episode / epoch_length)

                print(best_episode)
                print('epoch {ep}:\n\twins: {w}\n\ttotal win ratio: {wr}\n\tepoch win ratio: {ewr}'
                      .format(ep=epoch_number, w=wins, wr=(wins/episode), ewr=win_ratio))
                print('\tepsilon: {e}\n'.format(e=epsilon))
                break



    @staticmethod
    def action_list_to_string(action):
        return str(action) if type(action) == int else ''.join(str(tile).zfill(2) for tile in action)

    @staticmethod
    def string_to_action_list(s):
        if type(s) == int:
            return [s]
        return [int(s)] if len(s) == 2 else [int(s[:2]), int(s[2:])]

    def get_possible_next_actions(self, next_state, roll_sum):
        possible_actions_lists = self.env.get_possible_actions_for_roll(roll_sum=roll_sum)
        possible_actions = [self.action_list_to_string(action) for action in possible_actions_lists]
        return {action: self.q_table[next_state][action] for action in possible_actions}

    def build_q_table(self):
        all_states_binary_representations = [''.join(seq)
                                             for seq in itertools.product('01',
                                                                          repeat=self.env.action_space.tile_range[1])]

        possible_role_sums = self.env.action_space.get_all_possible_roll_sums()
        q_table = {'11111111111100': {self.action_list_to_string(action): 0.0
                                      for action in self.env.action_space.get_all_possible_tile_combinations()}}

        for state_binary_representation in all_states_binary_representations:
            for roll_sum in possible_role_sums:
                state_string = state_binary_representation + str(roll_sum).zfill(2)
                actions_for_roll_sum = self.env.action_space.get_actions_for_roll_sum(roll_sum=roll_sum)
                q_table[state_string] = {self.action_list_to_string(action): 0.0
                                         for action in actions_for_roll_sum}

        return q_table
