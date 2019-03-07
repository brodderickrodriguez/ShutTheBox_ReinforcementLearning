# Brodderick Rodriguez
# Auburn University - CSSE
# 04 Mar. 2019

from multiprocessing import Process
import ShutTheBox.agent.Agent as agnt
from ShutTheBox.agent import AgentConfiguration as Config


class MultiProcessTrain:
    def __init__(self):
        self.Q_TABLE_PATH = '/home/bcr0012/shut_the_box/ShutTheBox_ReinforcementLearning/ShutTheBox/agent/models/model.json'
        self.Q_TABLE_PATH = './agent/models/model.json'
        # self.q_table = Config.rw.read_q_table(self.Q_TABLE_PATH)

        self.q_table_path = Config.get_q_table_path()
        print(self.q_table_path)

        self.manager = Config.manager



    def train_agents(self, processes_count=1, iterations=10):

        for iteration in range(iterations):
            processes = []

            for i in range(processes_count):
                process = Process(target=self.train_single_agent)
                processes.append(process)
                process.start()

            for process in processes:
                process.join()


    def train_single_agent(self):
        # agent = agnt.Agent(self.Q_TABLE_PATH)
        agent = agnt.Agent()
        agent.learn()
        # Config.rw.aggregate_and_save_q_tables(agent.q_table, self.Q_TABLE)
        Config.rw._unsafe_write(agent.q_table, self.Q_TABLE_PATH)
