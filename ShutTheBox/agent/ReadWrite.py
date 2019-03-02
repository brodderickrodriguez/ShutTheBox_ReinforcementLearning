# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import json


write_flag = False


def read_q_func(f_name):
	while write_flag:
		pass

	with open(f_name) as f:
		data = json.load(f)
		for key in data:
			data[key] = {k: float(v) for k, v in data[key].items()}
	return data


def write_q_func(q_func, f_name):
    with open(f_name, 'w') as file:
        file.write(json.dumps(q_func))


def blend_and_save_q_fucs(q_func, f_name):
	write_flag = True
	other_q = read_q_func(f_name)
	for state in other_q:
		for action in other_q[state]:
			q_func[state][action] += other_q[state][action]
	write_q_func(q_func, f_name)
	write_flag = False
