# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019


import ShutTheBox.Agent as agnt

import shut_the_box_env.envs.ActionSpace as act


def action_to_string(action):
    return str(action) if type(action) == int else ''.join(str(tile).zfill(2) for tile in action)

def string_to_action(s):
    return [int(s)] if len(s) == 2 else [int(s[:2]), int(s[2:])]





# l = 11
# x = action_to_string(l)
# print(x)
#
# y = string_to_action(x)
# print(y)


def main():
    print('welcome Shut The Box')
    agent = agnt.Agent()


if __name__ == '__main__':
    main()
