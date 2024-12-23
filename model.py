import time
import importlib
from mesa import Model
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from wsn_message import WSNMessage 
from mesa.datacollection import DataCollector 
from agent import State 
import random

# Fonction utilitaire pour découper le nom de la classe
def split_on_last(string, char):
    rev_string = string[::-1]   # [::-1] obtient l'inverse de la chaîne
    end, start = rev_string.split(char, 1)
    return start[::-1], end[::-1]

class WSNModel(Model):
    def __init__(self, agents, width, height, sybil_ratio, normal_to_sybil_interaction_chance, confidence_score, seed=None):
        self.seed = seed
        if self.seed is None:
            self.seed = time.time()
        self.reset_randomizer(self.seed)

        # Initialisation du modèle
        self.running = True
        self.grid = SingleGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.sybil_ratio = sybil_ratio,
        self.normal_to_sybil_interaction_chance = normal_to_sybil_interaction_chance
        self.confidence_score = confidence_score
        
   # Initialiser le DataCollector
        self.datacollector = DataCollector(
            agent_reporters={
                "Position": lambda agent: (agent.pos if hasattr(agent, "pos") else None),
                "Type": lambda agent: type(agent).__name__,
                "IsSybil" : lambda agent: agent.state == State.SYBIL
            },
            
        ) 

        # Compter le nombre total d'agents
        self.num_nodes = 0

        # Ajout des agents
        for agent_class, agents in agents.items():
            module_name, class_name = split_on_last(agent_class, '.')
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            for agent in agents:
                a = cls(
                    agent["id"],
                    self,
                    agent["color"],
                    #self.sybil_ratio,
                    #self.normal_to_sybil_interaction_chance,
                    #self.confidence_score
                )
                self.schedule.add(a)
                self.grid.place_agent(a, (agent["x"], agent["y"]))
                self.num_nodes += 1  # Incrémenter le compteur pour chaque agent ajouté



    def step(self, messages):
        for i in range(0, len(messages)):
            wsnmessages = []
            for j in range(0, len(messages[i])):
                tempMess = messages[i][j]
                wsnmessages.append(WSNMessage(**tempMess))
            #self.schedule.agents[i].update_messages(wsnmessages)
        self.schedule.step()

    def run_model(self, n):
        for i in range(n):
            self.step()
