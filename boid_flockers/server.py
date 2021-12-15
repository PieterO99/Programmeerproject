from mesa.visualization.ModularVisualization import ModularServer

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas

from .environment import Door, Obstacle_Block
from .boid import Boid

def boid_draw(agent):
    if isinstance(agent, Obstacle_Block):
        return {"Shape": "rect", "w": 0.05, "h": 0.05, "Filled": "true", "Color": "Grey"}
    if isinstance(agent, Door):
        if agent.type == "revolving":
            return {"Shape": "circle", "r": 30, "Filled": "true", "Color": "Grey"}
        if agent.type == "normal":
            return {"Shape": "rect", "w": 0.01, "h": 0.1, "Filled": "true", "Color": "Grey"}
    if agent.destination[0] == 0:
        # return {"Shape": "rect", "w": 0.01, "h": 0.01, "Filled": "true", "Color": "Green"}
        return {"Shape": "rect", "w": 0.01, "h": 0.01, "Filled": "true", "Color": "Green"}
    else:
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": agent.closeness}

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 100,
    "width": 100,
    "height": 100,
    "speed": 1,
    "vision": 30,
    "separation": 5,
}

server = ModularServer(BoidFlockers, [boid_canvas], "Boids", model_params)