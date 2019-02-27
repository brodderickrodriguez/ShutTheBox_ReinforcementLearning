# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

# pycharm seems to want to delete this necessary import statement
# import shut_the_box_env.envs.ShutTheBoxEnv
import gym
import numpy as np
import itertools
from ShutTheBox.agent import Configuration as Config
import shut_the_box_env.envs.ShutTheBoxEnv


# Our decision making entity
class Agent:
    def __init__(self):
        self.env = gym.make('shut_the_box_env-v0')
        self.q_table = QTable.build(self.env)

    # returns a dictionary of possible actions with their corresponding values given a state and roll sum
    def get_possible_next_actions(self, next_state, roll_sum):
        # gets the list of possible actions from the environment given our roll sum
        possible_actions_lists = self.env.get_possible_actions_for_roll(roll_sum=roll_sum)

        # generates the strings associated with each action for Q(s, a)
        possible_actions = [QTable.action_list_to_string(action=action) for action in possible_actions_lists]

        # returns a dictionary of possible actions with their corresponding values
        return {action: self.q_table[next_state][action] for action in possible_actions}

    # runs a game episode and returns a string describing how the agent performed
    def run_single_episode(self, episode_number, epsilon):
        # reset the environment and set the state to a default initial state: '11111111111100'
        state = self.env.reset()

        # initialize variables to control this episode
        done, actions_taken, step_count, total_reward = False, [], 0, 0

        # get the initial roll in the form of <sum> = <die_1> + <die_2>
        roll_sum = self.env.roll_dice_get_sum()

        # get the first action to be performed via random sampling
        action = self.env.action_space.sample_action_from_roll_sum(roll_sum=roll_sum)

        # continue until we break when the 'done' flag is set
        while True:
            # append the action we are about to commit to the list of actions. Used for printing the episode
            actions_taken.append(action)

            # commit the action and get information from the environment
            next_state, reward, done, info = self.env.step(action=action)

            # get the roll sum from the environment
            roll_sum = info['next_roll']

            # increase step count and total reward based on information from the environment
            step_count += 1
            total_reward += reward

            # if 'done' flag is set, break this while loop and build our print string
            if done:
                break

            # get a dictionary of possible moves given our state and roll sum
            possible_actions = self.get_possible_next_actions(next_state=next_state,
                                                              roll_sum=roll_sum)

            # get the next action from the Q Learning algorithm using epsilon-greedy sampling
            next_action = Config.ra.next_action(possible_actions=possible_actions,
                                                epsilon=epsilon)

            # convert our environments action list to a string to key into our q table dictionary
            action = QTable.action_list_to_string(action=action)

            # update our q table according to Q Learning
            # https://en.wikipedia.org/wiki/Q-learning
            self.q_table[state][action] = Config.ra.get_new_q_value(q=self.q_table,
                                                                    state=state,
                                                                    action=action,
                                                                    next_reward=reward,
                                                                    next_state=next_state)

            # update our state action by parsing the action string back to an action list
            state = next_state
            action = QTable.string_to_action_list(action=next_action)

        # after breaking the loop, build a print string
        print_string = PrintStrings.build_episode_string(episode=episode_number,
                                                         actions=actions_taken,
                                                         step_count=step_count,
                                                         reward=reward,
                                                         tiles=self.env.tiles)

        # return information describing how our agent performed in this episode
        return total_reward, print_string, info['win']

    # performs infinite episodes using the same q table to 'learn' from
    def learn(self):
        print('learning...')
        # initialize some variables used to compute performance metrics
        episode, wins, win_ratio_list, best_episode, best_reward = 0, 0, [], None, float("-infinity")
        epoch_length = 10000

        # continue training forever...
        while True:
            # increment episodes and set a new epsilon for next episode
            episode += 1
            epsilon = 100 / np.sqrt(episode + 1)

            # perform an experiment and grab stats about how the agent performed
            reward, print_string, win = self.run_single_episode(episode_number=episode,
                                                                epsilon=epsilon)

            # increment wins accordingly
            wins += win
            win_ratio_list.append(win)

            # if we set a new record for reward achieved, save it
            if reward >= best_reward:
                best_episode, best_reward = print_string, reward

            # if the epoch is over, compute performance metrics and print them
            if episode % epoch_length == 0:
                # sum the number of wins in this epoch and compute a win ratio
                epoch_wins = sum(win_ratio_list)
                win_ratio_list = win_ratio_list[epoch_length:]
                epoch_win_ratio = epoch_wins / epoch_length

                # compute the total wins for this agent in every episode
                total_win_ratio = wins / episode

                # get an epoch number
                epoch = int(episode / epoch_length)

                # build a print string to output our performance so far
                s = PrintStrings.build_epoch_string(epoch=epoch,
                                                    episode=episode,
                                                    wins=wins,
                                                    epoch_wins=epoch_wins,
                                                    total_win_ratio=total_win_ratio,
                                                    epoch_win_ratio=epoch_win_ratio,
                                                    epsilon=epsilon)

                print(best_episode + '\n' + s + '\n')


# A static class which builds a q table and converts action strings to action lists and vise versa
class QTable:
    # builds the q table with (2^12) * 11 = 45,056 states and up to 11 actions per state
    @staticmethod
    def build(env):
        print('building q table')
        # generate all binary strings of length 12 to represent our states
        # each binary bit represents a tile in the Shut The Box game.
        # there are 12 tiles (1 - 12) so 2^12 possible strings
        states_in_binary = [''.join(seq) for seq in itertools.product('01', repeat=env.action_space.tile_range[1])]

        # get all possible roll sums: two die can add up to (2 - 12)
        possible_role_sums = env.action_space.get_all_possible_roll_sums()

        # initialize a generic initial state. '...00' represents die roll value of 0
        q_table = {'11111111111100': {QTable.action_list_to_string(action=action): 0.0
                                      for action in env.action_space.get_all_possible_tile_combinations()}}

        # for each binary representation of the Shut The Box game tiles, generate states accordingly
        for state_binary_representation in states_in_binary:
            # for each of the possible roll sums
            for roll_sum in possible_role_sums:
                # generate state string following the convention: 'bbbbbbbbbbddd', b is (0, 1), d is the roll sum
                state_string = state_binary_representation + str(roll_sum).zfill(2)

                # get the possible actions given a roll sum
                actions_for_roll_sum = env.action_space.get_actions_for_roll_sum(roll_sum=roll_sum)

                # build the state dictionary for this state string
                q_table[state_string] = {QTable.action_list_to_string(action=action): 0.0
                                         for action in actions_for_roll_sum}

        return q_table

    # converts an action list to an action string.
    # action lists are used in the environment and action string are used in the agent's q table
    @staticmethod
    def action_list_to_string(action):
        return str(action) if type(action) == int else ''.join(str(tile).zfill(2) for tile in action)

    # converts an action string to an action list
    # action lists are used in the environment and action string are used in the agent's q table
    @staticmethod
    def string_to_action_list(action):
        if type(action) == int:
            return [action]
        return [int(action)] if len(action) == 2 else [int(action[:2]), int(action[2:])]


# Simply generates print string to track our agent's performance
class PrintStrings:
    @staticmethod
    def build_episode_string(episode, actions, step_count, reward, tiles):
        return 'episode {i}:\n\t''actions:\t{a}\n\tstep_count:\t{sc}\n\ttiles:\t{et}\n\ttotal_reward:\t{tr}' \
            .format(i=episode, a=actions, sc=step_count, tr=reward, et=tiles)

    @staticmethod
    def build_epoch_string(epoch, episode, wins, epoch_wins, total_win_ratio, epoch_win_ratio, epsilon):
        return 'epoch {a} episode {b}:\n\ttotal wins {c}\n\tepoch wins {d}\n\ttotal win ratio {e}' \
               '\n\tepoch win ratio {f}\n\tepsilon {g}'.format(
                a=epoch, b=episode, c=wins, d=epoch_wins, e=total_win_ratio, f=epoch_win_ratio,
                g=epsilon)
