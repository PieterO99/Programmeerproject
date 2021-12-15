import numpy as np

from mesa import Agent
from .environment import Obstacle_Block

def bounded(self, pos):
        """
        Make sure position is between models bounds.
        """
        x,y = pos
        x = min(x, self.model.space.x_max-0.1)
        x = max(x, self.model.space.x_min)
        y = min(y, self.model.space.y_max-0.1)
        y = max(y, self.model.space.y_min)
        return np.array([x,y])

def difference(a,b):
    "returns positive number, the closer to zero, the more a and b are similar."
    cossim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return abs(1-cossim)

class Boid(Agent):
    """
    A Boid-style flocker agent.
    The agent follows three behaviors to flock:
        - Cohesion: steering towards neighboring agents.
        - Separation: avoiding getting too close to any other agent.
        - Alignment: try to fly in the same direction as the neighbors.
    Boids have a vision that defines the radius in which they look for their
    neighbors to flock with. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        # added destination
        destination,
        speed,
        velocity,
        vision,
        separation,
        separate=0.25,
        match=0.04,
        # added destination
        approach_destination=0.05
    ):
        """
        Create a new Boid flocker agent.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.
            heading: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids.
            separation: Minimum distance to maintain from other Boids.
            cohere: the relative importance of matching neighbors' positions
            separate: the relative importance of avoiding close neighbors
            match: the relative importance of matching neighbors' headings
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        # added destination
        self.destination = np.array(destination)
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.separate_factor = separate
        self.match_factor = match
        # added destination
        self.destination_factor = approach_destination

    def separate(self, neighbors):
        """
        Return a vector away from any neighbors closer than separation dist.
        Idee: vertragen als mensen te dichtbij komen, afhankelijk van hoe sigma de agent is: berekenen vanuit speed, velocity en pos?
        """
        me = self.pos
        obstacles = []
        neighbor_boids = []
        for neighbor in neighbors:
            if isinstance(neighbor, Obstacle_Block):
                obstacles.append(neighbor)
            elif isinstance(neighbor, Boid):
                neighbor_boids.append(neighbor)
        
        separation_vector = np.zeros(2)

        # avoid all obstacles within vision, relative to distance
        prediction_pos = self.pos + self.speed * self.velocity

        for other in obstacles:
            predicted_obstacle_distance = self.model.space.get_distance(prediction_pos, other.pos)
            # may add tolerable distance to obstacle to use instead of vision
            if predicted_obstacle_distance < self.vision:
                v = self.model.space.get_heading(me, other.pos)
                # choose perp that's most in line with destination based on cosine similarity
                pref_perp_v = np.array([-1*v[1],v[0]])
                destination_v = self.destination-self.pos
                if difference(pref_perp_v, destination_v) > difference(-pref_perp_v, destination_v):
                    pref_perp_v *= -1

                separation_vector += pref_perp_v / (predicted_obstacle_distance)

        # separate from neighbors
        for other in neighbor_boids:
            # predict if boid and neighbor will come too close
            prediction_pos_neighbor = other.pos + other.speed * other.velocity
            prediction_separation = self.model.space.get_distance(prediction_pos, prediction_pos_neighbor)

            # if so, go in opposite direction of predicted difference vector, also weigh by predicted distance
            if prediction_separation < self.separation:
                prediction_difference_vector = prediction_pos_neighbor - prediction_pos
                perp = [-prediction_difference_vector[1], prediction_difference_vector[0]]
                # divide by square to weigh normalized vector by 1/prediction_separation
                separation_vector += perp / (prediction_separation)
                
        return separation_vector

    def match_heading(self, neighbors):
        """
        Return a vector of the neighbors' average heading.
        """
        match_vector = np.zeros(2)
        if neighbors:
            for neighbor in neighbors:
                match_vector += neighbor.velocity if isinstance(neighbor, Boid) else 0
            match_vector /= len(neighbors)
        return match_vector


    def approach_destination(self):
        return self.destination - self.pos
        

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """

        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity = (
            + self.separate(neighbors) * self.separate_factor
            + self.match_heading(neighbors) * self.match_factor
            + self.approach_destination() * self.destination_factor
        ) / 2
        self.velocity = (self.velocity / np.linalg.norm(self.velocity) if (self.velocity).all() != 0 else 0)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, bounded(self, new_pos))
        if np.allclose(self.pos, self.destination, atol=5):
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
