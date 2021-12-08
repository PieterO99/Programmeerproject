from mesa.visualization.ModularVisualization import ModularServer

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas

from .environment import Door
from .boid import Boid

def boid_draw(agent):
    if isinstance(agent, Door):
        return {"Shape": "rect", "w": 0.1, "h": 0.1, "Filled": "true", "Color": "Brown"}
    if agent.destination[0] == 0:
        return {"Shape": "rect", "w": 0.01, "h": 0.01, "Filled": "true", "Color": "Green"}
    else:
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Blue"}

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 100,
    "width": 100,
    "height": 100,
    "speed": 2,
    "vision": 10,
    "separation": 2,
}

server = ModularServer(BoidFlockers, [boid_canvas], "Boids", model_params)