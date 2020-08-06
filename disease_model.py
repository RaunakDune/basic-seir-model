from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.batchrunner import BatchRunner

from itertools import cycle
import random

stages = ['S','E','I','R']

class DiseaseAgent(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        if random.randint(0,100) < 10:
            self.state = 2
        else:
            self.state = random.randint(0, 1)
    
    def step(self):
        self.move()
        if self.state < 4:
            self.spread_disease()
    
    def spread_disease(self):
        neighbours = self.model.grid.get_cell_list_contents([self.pos])

        if (len(neighbours) > 1):
            next_agent = self.random.choice(neighbours)
            if self.state == 3:
                return
            if next_agent.state == 3 and self.state != 3:
                self.state = (self.state + 1) % 4
                return
            if (next_agent.state > 1) and (self.state == 0):
                self.state += 1
                return
            if (next_agent.state == 0) and (self.state > 1):
                next_agent.state += 1
                return
            next_agent.state = (next_agent.state + 1) % 4
            self.state = (self.state + 1) % 4
    
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
        

class DiseaseModel(Model):
    def __init__(self, N, width, height):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)
        self.schedule = RandomActivation(self)
        self.running = True

        for i in range(self.num_agents):
            a = DiseaseAgent(i, self)
            self.schedule.add(a)

            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(a, (x, y))
            self.datacollector = DataCollector(
                agent_reporters={"State":"state"}
            )
    
    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()