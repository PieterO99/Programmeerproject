from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np

# constants need to be between 0 and 1.
burn_const_dict = {"acacia": 1, "oak": 0.9, "pine": 0.6}
burn_time_dict = {"acacia": 15, "oak": 20, "pine": 40}
tree_color_dict = {"acacia": "#117a65", "oak": "#229954" , "pine": "#145a32"}
burn_color_dict = {"acacia": "#d35400", "oak": "#f1c40f" , "pine": "#a93226"}


class TreeAgent(Agent):
    """ A tree that can burn (down)."""
    def __init__(self, unique_id, model, status, tree_type):
        super().__init__(unique_id, model)
        # standard, burning, empty
        self.status = status
        self.tree_type = tree_type
        assert self.status in ["std", "burning", "empty"]
        print('yeet')
        
        self.steps_left = burn_time_dict[self.tree_type]

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
            chance_to_burn = burn_const_dict[self.tree_type] * burning_neighbours / len(neighbours)
            self.status = (self.random.choices(["burning", "std"], [chance_to_burn, 1-chance_to_burn], k=1))[0]

    def step(self):
        self.burn()

class ForestFireModel(Model):
    """A model with some number of agents."""
    def __init__(self, density, width, height, trees_burning, flora_dict):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.running = True

        # Create agents
        tree_places = self.random.choices(range(width * height), weights=([1] * width * height), k=int(density * width * height))
        for i in range(width * height):
            if i < trees_burning:
                flora_types = list(flora_dict)
                flora_weights = [flora_dict[flora_type] for flora_type in flora_types]
                a = TreeAgent(i, self, "burning", self.random.choices(flora_types, weights=flora_weights, k=1)[0])
            elif i in tree_places:
                a = TreeAgent(i, self, "std", self.random.choices(flora_types, weights=flora_weights, k=1)[0])
            else:
                a = TreeAgent(i, self, "empty", "oak")
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = i % width
            y = i // width
            self.grid.place_agent(a, (x, y))

    def step(self):
        self.schedule.step()