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
from mesa.datacollection import DataCollector

from .boid import Boid
from .environment import (Door, Obstacle_Block)

class BoidFlockers(Model):
    """
    Flocker model class. Handles agent creation, placement and scheduling.
    """

    def __init__(
        self,
        population=20,
        collissions = 0,
        width=100,
        height=100,
        speed=0.2,
        vision=10,
        separation=2,
        separate_factor=0.2,
        distance_factor=1,
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
        self.collissions = collissions
        self.vision = vision
        self.speed = speed
        self.separation = separation
        self.boids_count = 0
        self.schedule = RandomActivation(self)
        self.space = ContinuousSpace(width, height, False) 
        self.factors = dict(separate_factor=separate_factor, distance_factor=distance_factor, match=match, approach_destination=approach_destination)
        self.doors = [Door(self.population+1, self, (0.3*self.space.x_max, 0), "revolving"), 
                Door(self.population+2, self, (0.5*self.space.x_max, 0), "revolving"),
                Door(self.population+3, self,(0.3*self.space.x_max, self.space.y_max - 0.1), "revolving"),
                Door(self.population+4, self, (0, 0.1*self.space.y_max), "normal"),
                Door(self.population+5, self, (0, 0.7*self.space.y_max), "normal")]
        self.make_agents()
        self.running = True

    def make_agents(self):
        """
        Create self.population agents, with random positions and starting headings.
        """

        # add doors
        for door in self.doors:
            self.schedule.add(door)

        # add agents
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
            self.boids_count += 1

            print([boid.distance_factor, boid.separate_factor])

        # add student helpdesk
        ID = self.population+7
        top_left_corner = np.array((self.space.x_max*0.4, self.space.y_max*0.4))
        helpdesk_width = 30
        helpdesk_height = 20
        for i in range(helpdesk_width):
            for j in range(helpdesk_height):
                pos = np.array((i*self.space.x_max / 100, j*self.space.y_max / 100))
                block = Obstacle_Block(ID+helpdesk_height*i+j, self, top_left_corner + pos)
                self.schedule.add(block)
                self.space.place_agent(block, block.pos)

        # add walls
        ID += helpdesk_height *helpdesk_width
        w = self.space.width
        h = self.space.height
        for i in range(w):
            block1 = Obstacle_Block(ID+i, self, np.array([i,0]))
            block2 = Obstacle_Block(ID+w+i, self, np.array([i,h-1]))
            self.schedule.add(block1)
            self.space.place_agent(block1, block1.pos)
            self.schedule.add(block2)
            self.space.place_agent(block2, block2.pos)

        ID += 2*w
        for i in range(h):
            block1 = Obstacle_Block(ID+i, self, np.array([0,i]))
            block2 = Obstacle_Block(ID+h+i, self, np.array([w-1,i]))
            self.schedule.add(block1)
            self.space.place_agent(block1, block1.pos)
            self.schedule.add(block2)
            self.space.place_agent(block2, block2.pos)

        # collect data
        self.datacollector = DataCollector(
            model_reporters={"Collisions": "collissions"})

    def step(self):
        self.datacollector.collect(self)
        self.schedule.step()
        if self.boids_count == 0:
            self.running = False