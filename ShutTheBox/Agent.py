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
        self.q_table = QTable.build(self.env)

    def run_single_episode(self, episode_number, epsilon):
        state = self.env.reset()
        done, actions_taken, step_count, total_reward = False, [], 0, 0
        roll_sum = self.env.roll_dice_get_sum()
        action = self.env.action_space.sample_action_from_roll_sum(roll_sum=roll_sum)

        while True:
            actions_taken.append(action)
            next_state, reward, done, info = self.env.step(action=action)
            roll_sum = info['next_roll']
            step_count += 1
            total_reward += reward

            if done: break

            possible_actions = self.get_possible_next_actions(next_state=next_state,
                                                              roll_sum=roll_sum)

            next_action = Config.ra.next_action(possible_actions=possible_actions,
                                                epsilon=epsilon)

            action = QTable.action_list_to_string(action=action)

            self.q_table[state][action] = Config.ra.get_new_q_value(q=self.q_table,
                                                                    state=state,
                                                                    action=action,
                                                                    next_reward=reward,
                                                                    next_state=next_state)

            state = next_state
            action = QTable.string_to_action_list(action=next_action)

        print_string = PrintStrings.build_episode_string(episode=episode_number,
                                                         actions=actions_taken,
                                                         step_count=step_count,
                                                         reward=reward,
                                                         tiles=self.env.tiles)

        return total_reward, print_string, info['win']

    def get_possible_next_actions(self, next_state, roll_sum):
        possible_actions_lists = self.env.get_possible_actions_for_roll(roll_sum=roll_sum)

        possible_actions = [QTable.action_list_to_string(action=action)
                            for action in possible_actions_lists]

        return {action: self.q_table[next_state][action]
                for action in possible_actions}

    def learn(self):
        print('learning...')
        episode, wins, win_ratio_list, best_episode, best_reward, epoch_length = 0, 0, [], None, float("-infinity"), 0

        while True:
            episode += 1
            epsilon = 100 / np.sqrt(episode + 1)
            reward, print_string, win = self.run_single_episode(episode_number=episode,
                                                                epsilon=epsilon)
            wins += win
            win_ratio_list.append(win)

            if reward >= best_reward:
                best_episode, best_reward = print_string, reward

            if episode % epoch_length == 0:
                epoch_wins = sum(win_ratio_list)
                epoch_win_ratio = epoch_wins / epoch_length
                total_win_ratio = wins / episode
                epoch = int(episode / epoch_length)
                win_ratio_list = win_ratio_list[epoch_length:]

                s = PrintStrings.build_epoch_string(epoch=epoch,
                                                    episode=episode,
                                                    wins=wins,
                                                    epoch_wins=epoch_wins,
                                                    total_win_ratio=total_win_ratio,
                                                    epoch_win_ratio=epoch_win_ratio,
                                                    epsilon=epsilon)

                print(best_episode + '\n' + s + '\n')


class QTable:
    @staticmethod
    def build(env):
        print('building q table')
        states_in_binary = [''.join(seq) for seq in itertools.product('01', repeat=env.action_space.tile_range[1])]
        possible_role_sums = env.action_space.get_all_possible_roll_sums()
        q_table = {'11111111111100': {QTable.action_list_to_string(action=action): 0.0
                                      for action in env.action_space.get_all_possible_tile_combinations()}}

        for state_binary_representation in states_in_binary:
            for roll_sum in possible_role_sums:
                state_string = state_binary_representation + str(roll_sum).zfill(2)
                actions_for_roll_sum = env.action_space.get_actions_for_roll_sum(roll_sum=roll_sum)
                q_table[state_string] = {QTable.action_list_to_string(action=action): 0.0
                                         for action in actions_for_roll_sum}

        return q_table

    @staticmethod
    def action_list_to_string(action):
        return str(action) if type(action) == int else ''.join(str(tile).zfill(2) for tile in action)

    @staticmethod
    def string_to_action_list(action):
        if type(action) == int:
            return [action]
        return [int(action)] if len(action) == 2 else [int(action[:2]), int(action[2:])]


class PrintStrings:
    @staticmethod
    def build_episode_string(episode, actions, step_count, reward, tiles):
        return 'episode {i}:\n\t''actions:\t{a}\n\tstep_count:\t{sc}\n\ttiles:\t{et}\n\ttotal_reward:\t{tr}'\
            .format(i=episode, a=actions, sc=step_count, tr=reward, et=tiles)

    @staticmethod
    def build_epoch_string(epoch, episode, wins, epoch_wins, total_win_ratio, epoch_win_ratio, epsilon):
        return 'epoch {a} episode {b}:\n\ttotal wins {c}\n\tepoch wins {d}\n\ttotal win ratio {e}' \
               '\n\tepoch win ratio {f}\n\tepsilon {g}'.format(
                a=epoch, b=episode, c=wins, d=epoch_wins, e=total_win_ratio, f=epoch_win_ratio,
                g=epsilon)
