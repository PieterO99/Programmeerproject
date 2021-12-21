import numpy as np

from mesa import Agent
from .environment import Obstacle_Block


TOLERABLE_DISTANCE_BETWEEN_BOIDS = 0.1


def bounded(self, pos):
    """
    Force position 'pos' to be between models bounds.
    """
    x, y = pos
    x = min(x, self.model.space.x_max - 0.1)
    x = max(x, self.model.space.x_min)
    y = min(y, self.model.space.y_max - 0.1)
    y = max(y, self.model.space.y_min)
    return np.array([x, y])


def difference(a, b):
    """
    returns positive number, the closer to zero, the more a and b are similar.
    """
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cossim = np.dot(a, b) / (norma * normb) if (norma != 0 and normb != 0) else 0
    return abs(1 - cossim)


class Boid(Agent):
    """
    A moving agent with a destination, inspired by the boid-model.
    The agent follows two behaviors to move:
        - Avoidance: avoiding neighbors and obstacles.
        - Moving to destination: steering to destination.
    Boids have a vision that defines the radius in which they look for their
    neighbors and obstacles. Their speed (a scalar) and velocity (a vector)
    define their movement. Separation is their desired minimum distance from
    any other Boid.
    """

    def __init__(
        self,
        unique_id,
        model,
        pos,
        destination,
        speed,
        velocity,
        vision,
        separation,
        collissions=0,
        steps_until_dest=0,
        separate_factor=0.25,
        distance_factor=1,
        approach_destination=0.05
    ):
        """
        Create a new Boid agent.
        Args:
            unique_id: Unique agent identifyer.
            pos: Starting position
            speed: Distance to move per step.
            velocity: numpy vector for the Boid's direction of movement.
            vision: Radius to look around for nearby Boids and obstacles.
            separation: Minimum distance to maintain from other Boids.
            separate_factor: the relative importance of avoiding close neighbors
            distance_factor: power by which we weigh the closeness of neighbors to avoid them
            destination_factor: the relative importance of steering towards destination
        """
        super().__init__(unique_id, model)
        self.pos = np.array(pos)
        self.collissions = collissions
        self.destination = destination
        self.speed = speed
        self.velocity = velocity
        self.vision = vision
        self.separation = separation
        self.steps_until_dest = steps_until_dest
        self.separate_factor = separate_factor
        self.distance_factor = distance_factor
        self.destination_factor = approach_destination

    def avoid(self, neighbors):
        """
        Return a vector away from any neighbors or obstacles closer than separation distance.
        """
        me = self.pos
        obstacles = []
        neighbor_boids = []
        for neighbor in neighbors:
            if isinstance(neighbor, Obstacle_Block):
                obstacles.append(neighbor)
            elif isinstance(neighbor, Boid):
                neighbor_boids.append(neighbor)

        obs_separation_vector = np.zeros(2)
        neighbor_separation_vector = np.zeros(2)

        # avoid all obstacles within vision, relative to distance
        prediction_pos = self.pos + self.speed * self.velocity

        for other in obstacles:
            predicted_obstacle_distance = self.model.space.get_distance(prediction_pos, other.pos)
            # may add tolerable distance to obstacle to use instead of vision
            if predicted_obstacle_distance < self.vision:
                v = self.model.space.get_heading(me, other.pos)
                # choose perp that's most in line with destination based on cosine similarity
                pref_perp_v = np.array([-1 * v[1], v[0]])
                destination_v = self.destination.pos - self.pos
                if difference(pref_perp_v, destination_v) > difference(-pref_perp_v, destination_v):
                    pref_perp_v *= -1

                obs_separation_vector += pref_perp_v / (predicted_obstacle_distance)**2

        # separate from neighbors
        for other in neighbor_boids:
            # count collissions
            if self.model.space.get_distance(self.pos, other.pos) < TOLERABLE_DISTANCE_BETWEEN_BOIDS:
                self.model.collissions += 0.5

            # predict if boid and neighbor will come too close
            prediction_pos_neighbor = other.pos + other.speed * other.velocity
            prediction_separation = self.model.space.get_distance(prediction_pos, prediction_pos_neighbor)

            # if so, go in opposite direction of predicted difference vector, also weigh by predicted distance
            if prediction_separation < self.separation:
                prediction_difference_vector = prediction_pos_neighbor - prediction_pos
                # make people avoid each other counter-clockwise
                perp = [prediction_difference_vector[1], -prediction_difference_vector[0]]
                # divide by distance_factor+1 to weigh normalized vector by 1/prediction_separation^(distance_factor)
                neighbor_separation_vector += perp / (prediction_separation)**(self.distance_factor + 1)

        return np.array(obs_separation_vector) + np.array(neighbor_separation_vector)

    def approach_destination(self):
        return np.array(self.destination.pos) - self.pos

    def step(self):
        """
        Get the Boid's neighbors, compute the new vector, and move accordingly.
        """
        neighbors = self.model.space.get_neighbors(self.pos, self.vision, False)
        self.velocity = (
            + self.avoid(neighbors) * self.separate_factor
            + self.approach_destination() * self.destination_factor
        ) / 2
        self.velocity = (self.velocity / np.linalg.norm(self.velocity) if (self.velocity).all() != 0 else 0)
        new_pos = self.pos + self.velocity * self.speed
        self.model.space.move_agent(self, bounded(self, new_pos))
        self.steps_until_dest += 1

        if np.allclose(self.pos, self.destination.pos, atol=5):
            self.model.flow += (self.steps_until_dest / self.speed[0]) / self.model.population
            self.model.space.remove_agent(self)
            self.model.schedule.remove(self)
            self.model.boids_count -= 1
