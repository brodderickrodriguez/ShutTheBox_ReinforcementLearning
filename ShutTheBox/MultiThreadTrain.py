# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import threading
import time
import ShutTheBox.agent.Agent as agnt
import ShutTheBox.agent.ReadWrite as rw


def train_single_agent():
	agent = agnt.Agent()
	agent.learn()
	rw.blend_and_save_q_fucs(agent.q_table, './agent/models/model.json')


def train(n):
	thread_lock = threading.Lock()
	threads = []

	while True:
		for n in range(10):
			thread = threading.Thread(target=train_single_agent)
			thread.start()
			threads.append(thread)

		for thread in threads:
			thread.join()
