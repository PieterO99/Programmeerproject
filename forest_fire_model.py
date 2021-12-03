from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np

def compute_density(model):
    statuses = [agent.status for agent in model.schedule.agents]
    burning = statuses.count("burning")
    empty = statuses.count("empty")
    standard = statuses.count("std")
    return (standard / (standard + empty + burning))

class TreeAgent(Agent):
    """ A tree that can burn (down)."""
    def __init__(self, unique_id, model, status):
        super().__init__(unique_id, model)
        # standard, burning, empty
        self.status = status
        assert self.status in ["std", "burning", "empty"]
        # a tree keeps burning for 5 steps until it collapses
        self.steps_left = 20

    def burn(self):
        neighbours = self.model.grid.get_neighbors(self.pos, moore=True, radius=1)
        burning_neighbours = 0
        for neighbour in neighbours:
            if neighbour.status == "burning":
                burning_neighbours += 1
        if self.status == "burning":
            self.steps_left -= 1
            if self.steps_left == 0:
                self.status = "empty"
        elif self.status == "std":
            chance_to_burn = burning_neighbours / len(neighbours)
            self.status = (self.random.choices(["burning", "std"], [chance_to_burn, 1-chance_to_burn], k=1))[0]

    def step(self):
        self.burn()

class ForestFireModel(Model):
    """A model with some number of agents."""
    def __init__(self, density, width, height, trees_burning):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        tree_places = self.random.choices(range(width * height), weights=([1] * width * height), k=int(density * width * height))
        for i in range(width * height):
            if i < trees_burning:
                a = TreeAgent(i, self, "burning")
            elif i in tree_places:
                a = TreeAgent(i, self, "std")
            else:
                a = TreeAgent(i, self, "empty")
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = i % width
            y = i // width
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"EndDensity": compute_density},
            agent_reporters={"Status": "status"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()