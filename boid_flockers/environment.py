import numpy as np

from mesa import Agent


class Door(Agent):
    def __init__(self, unique_id, model, pos, type):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.type = type


class Obstacle_Block(Agent):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
