from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

from disease_model import *

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "r": 0.7}

    if agent.state == 0:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.state == 1:
        portrayal["Color"] = "orange"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    elif agent.state == 2:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.6
    elif agent.state == 3:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.7
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 900, 800)

server = ModularServer(DiseaseModel,
                       [grid],
                       "SEIR Disease Model",
                       {"N":200, "width":50, "height":50})
server.port = 8521 # The default
server.launch()