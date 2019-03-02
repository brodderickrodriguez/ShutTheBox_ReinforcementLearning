# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import threading
import time
import ShutTheBox.agent.Agent as agnt
import ShutTheBox.agent.ReadWrite as rw


Q_TABLE = '/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/agent/models/model.json'
# Q_TABLE = './agent/models/model.json'

# TODO: implement multiprocessing
# NOTE: this module no longer learns a model using multi threading

def train_single_agent():
	agent = agnt.Agent(Q_TABLE)
	agent.learn()

	rw.write_q_func(agent.q_table, Q_TABLE)
	# rw.blend_and_save_q_fucs(agent.q_table, Q_TABLE)


# def train(n):
# 	thread_lock = threading.Lock()
# 	threads = []
# 	agents = []
#
# 	while True:
# 		for n in range(10):
# 			thread = threading.Thread(target=train_single_agent)
# 			thread.start()
# 			threads.append(thread)
#
# 		for thread in threads:
# 			thread.join()
#
# 		threads = threads[:10]



def train(n):
	for i in range(n):
		print('iteration {i} of {n}'.format(i=i, n=n))
		train_single_agent()
