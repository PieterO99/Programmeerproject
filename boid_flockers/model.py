"""
Flockers
=============================================================
A Mesa implementation of Craig Reynolds's Boids flocker model.
Uses numpy arrays to represent vectors.
"""

import numpy as np
import random

from mesa import Model
from mesa.space import ContinuousSpace
from mesa.time import RandomActivation

from .boid import Boid
from .environment import Door

class BoidFlockers(Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        population=20,
        width=100,
        height=100,
        speed=1,
        vision=10,
        separation=5,
        cohere=0.025,
        separate=0.5,
        match=0.04,
        approach_destination=0.1
    ):
        """
        Create a new Flockers model.
        Args:
            population: Number of Boids
            width, height: Size of the space.
            speed: How fast should the Boids move.
            vision: How far around should each Boid look for its neighbors
            separation: What's the minimum distance each Boid will attempt to
                    keep from any other
            cohere, separate, match: factors for the relative importance of
                    the three drives."""
        self.population = population
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, False) 
        self.factors = dict(cohere=cohere, separate=separate, match=match, approach_destination=approach_destination)
        self.doors = [Door(self.population+1, self, (0.3*self.space.x_max, self.space.y_max - 0.1)), 
                Door(self.population+2, self, (0.5*self.space.x_max, self.space.y_max - 0.1)),
                Door(self.population+3, self,(0.3*self.space.x_max, 0)),
                Door(self.population+4, self, (0, 0.1*self.space.y_max)),
                Door(self.population+5, self, (0, 0.7*self.space.y_max))]
        self.make_agents()
        self.running = True

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """
        for door in self.doors:
            self.schedule.add(door)
        for i in range(self.population):
            doors = random.choices(self.doors, [1]*len(self.doors), k=2)
            pos = doors[0].pos
            destination = doors[1].pos
            velocity = np.random.random(2) * 2 - 1
            boid = Boid(
                i,
                self,
                pos,
                destination,
                self.speed,
                velocity,
                self.vision,
                self.separation,
                **self.factors
            )
            self.space.place_agent(boid, pos)
            self.schedule.add(boid)

    def step(self):
        self.schedule.step()