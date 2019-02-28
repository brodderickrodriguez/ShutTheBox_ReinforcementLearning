# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import threading
import time
import ShutTheBox.agent.Agent as agnt
import ShutTheBox.agent.ReadWrite as rw


Q_TABLE = '/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/agent/models/model.json'
# Q_TABLE = './agent/models/model.json'


def train_single_agent():
	agent = agnt.Agent()
	agent.learn()
	rw.blend_and_save_q_fucs(agent.q_table, Q_TABLE)


def train(n):
	thread_lock = threading.Lock()
	threads = []
	agents = []

	while True:
		for n in range(10):
			thread = threading.Thread(target=train_single_agent)
			thread.start()
			threads.append(thread)

		for thread in threads:
			thread.join()

		threads = threads[:10]
