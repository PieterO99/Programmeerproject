from mesa.visualization.ModularVisualization import ModularServer

from .model import BoidFlockers
from .SimpleContinuousModule import SimpleCanvas

from .environment import Door


def boid_draw(agent):
    if agent.destination[0] == 0:
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Red"}
    else:
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": "Blue"}

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 40,
    "width": 100,
    "height": 100,
    "speed": 2,
    "vision": 10,
    "separation": 2,
}

server = ModularServer(BoidFlockers, [boid_canvas], "Boids", model_params)