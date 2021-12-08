import numpy as np

from mesa import Agent

class Door(Agent):
    def __init__(self, pos: "tuple"):
        self.pos = np.array(pos)
