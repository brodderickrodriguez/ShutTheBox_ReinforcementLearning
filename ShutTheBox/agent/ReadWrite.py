# Brodderick Rodriguez
# Auburn University - CSSE
# 26 Feb. 2019

import json


class ReadWrite:
	WRITE_FLAG = False

	def __init__(self):
		pass

	@staticmethod
	def _unsafe_write(q_table, file_name):
		with open(file_name, 'w') as file:
			file.write(json.dumps(q_table))

	@staticmethod
	def _unsafe_read(file_name):
		with open(file_name) as f:
			data = json.load(f)
			for key in data:
				data[key] = {k: float(v) for k, v in data[key].items()}
		return data

	@staticmethod
	def read_q_table(file_name):
		while ReadWrite.WRITE_FLAG:
			print('in read - flag=TRUE')
			pass

		data = ReadWrite._unsafe_read(file_name)

		return data

	@staticmethod
	def aggregate_and_save_q_tables(q_table, file_name):
		while ReadWrite.WRITE_FLAG:
			print('in read - flag=TRUE')
			pass

		ReadWrite.WRITE_FLAG = True

		other_q = ReadWrite._unsafe_read(file_name)

		for state in other_q:
			for action in other_q[state]:
				q_table[state][action] += other_q[state][action]

		ReadWrite._unsafe_write(q_table, file_name)

		ReadWrite.WRITE_FLAG = False
