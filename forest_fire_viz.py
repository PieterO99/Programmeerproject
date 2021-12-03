from forest_fire_model import *
import matplotlib.pyplot as plt
import numpy as np
from mesa.batchrunner import BatchRunner
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer


def agent_portrayal(agent):
    if agent.status == "std":
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "green",
                    "w": 1,
                    "h": 1}
    elif agent.status == "burning":
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "red",
                    "w": 1,
                    "h": 1}
    elif agent.status == "empty":
        portrayal = {"Shape": "circle",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": "white",
                    "r": 0.5}
    return portrayal

grid = CanvasGrid(agent_portrayal, 50, 50, 500, 500)
server = ModularServer(ForestFireModel,
                       [grid],
                       "Forest Fire Model",
                       {"density":0.7, "width":50, "height":50, "trees_burning": 50})
server.port = 8521 # The default
server.launch()