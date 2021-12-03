from forest_fire_model import (tree_color_dict, burn_color_dict, ForestFireModel)
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
                    "Color": tree_color_dict[agent.tree_type],
                    "w": 1,
                    "h": 1}
    elif agent.status == "burning":
        portrayal = {"Shape": "rect",
                    "Filled": "true",
                    "Layer": 0,
                    "Color": burn_color_dict[agent.tree_type],
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
                       {"density":0.7, "width":50, "height":50, "trees_burning": 50, 
                       "flora_dict": {"acacia": 0.3, "oak": 0.6, "pine": 0.1}})
server.port = 8521 # The default
server.launch()