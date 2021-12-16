from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas

from .environment import Door, Obstacle_Block
from .boid import Boid

def boid_draw(agent):

    if isinstance(agent, Door):
        if agent.type == "revolving":
            return {"Shape": "circle", "r": 30, "Filled": "true", "Color": "Black"}
        elif agent.type == "normal":
            return {"Shape": "rect", "w": 0.1, "h": 0.1, "Filled": "true", "Color": "Black"}
    elif isinstance(agent, Obstacle_Block):
        return {"Shape": "rect", "w": 0.05, "h": 0.05, "Filled": "true", "Color": "Grey"}
    elif agent.destination[0] == 0:
        return {"Shape": "rect", "w": 0.01, "h": 0.01, "Filled": "true", "Color": " #a93226"}
    else:
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "#f1c40f"}

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 100,
    "width": 100,
    "height": 100,
    "speed": 1,
    "vision": 30,
    "separation": 5,
}

chart_element = ChartModule([{"Label": "Collisions", "Color": "Black"}])

server = ModularServer(BoidFlockers, [boid_canvas, chart_element], "Boids", model_params)