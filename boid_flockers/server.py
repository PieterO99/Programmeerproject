from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import ChartModule
from mesa.visualization.UserParam import UserSettableParameter

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
    else:
        color = "Black"
        if agent.destination.unique_id == "door_a": 
            color = "#f1c40f"
        elif agent.destination.unique_id == "door_b": 
            color = "#d68910"
        elif agent.destination.unique_id == "door_c": 
            color = "#935116"
        elif agent.destination.unique_id == "door_d": 
            color = "#f1948a"
        elif agent.destination.unique_id == "door_e": 
            color = "#78281f"
        return {"Shape": "circle", "r": 2, "Filled": "true", "Color": color}

boid_canvas = SimpleCanvas(boid_draw, 500, 500)
model_params = {
    "population": 50,
    "width": 100,
    "height": 100,
    "speed": 1,
    "vision": 30,
    "separation": UserSettableParameter(
        "slider", "Distance to maintain", 1.5, 0.5, 10, 0.5
    ),
    "separate_factor": UserSettableParameter(
        "slider", "Avoidance factor", 0.2, 0, 2, 0.1
    ),
    "distance_factor": UserSettableParameter(
        "slider", "Distance factor", 1.0, 0.0, 3.0, 0.1
    )
}

chart_element = ChartModule([{"Label": "Collisions", "Color": "Black"}])

server = ModularServer(BoidFlockers, [boid_canvas, chart_element], "Boids", model_params)