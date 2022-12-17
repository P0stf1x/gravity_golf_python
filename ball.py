import math
import numpy as np
from defaults import hex2rgb, rgb2hex

def boundingboxes_intersects(box1, box2):
    inversed_intersection = False
    inversed_intersection += not (box1["left"] < box2["right"])
    inversed_intersection += not (box1["top"] < box2["down"])
    inversed_intersection += not (box1["right"] > box2["left"])
    inversed_intersection += not (box1["down"] > box2["top"])

    return not inversed_intersection

class Ball:
    def __init__(self, start_position, freeze_ball, collision_enabled) -> None:
        self.color = "#FFFFFF"
        self.radius = 10
        self.position = np.array(start_position)
        self.acceleration = np.array([0.0, 0.0])
        self.speed = np.array([0.0, 0.0])
        self.update_boundingbox()
        self.freeze_ball = freeze_ball
        self.collision_enabled = collision_enabled

    def update_boundingbox(self):
        self.boundingbox_coordinates = ((self.position[0] - self.radius, self.position[1] - self.radius), (self.position[0] + self.radius, self.position[1] + self.radius))
        self.boundingbox = {
            "left": self.position[0] - self.radius,
            "right": self.position[0] + self.radius,
            "top": self.position[1] - self.radius,
            "down": self.position[1] + self.radius,
        }

    def physics(self, deltatime, fps, planets=[]):
        if fps == 0:
            fps = 1
        self.speed += self.acceleration * deltatime
        self.position += self.speed
        self.acceleration = np.array([0., 0.])
        self.update_boundingbox()
        for planet in planets:
            # Gravity physics
            if not self.freeze_ball:
                radius = ((1e-0) * deltatime * ((10 * planet.mass)/(math.sqrt((planet.position[1] - self.position[1])**2 + (planet.position[0] - self.position[0])**2))))**2
            else:
                radius = 0
            degrees = math.atan2(planet.position[1] - self.position[1], planet.position[0] - self.position[0])
            self.acceleration += self.polar2decart((radius, degrees))
            
            # Intersection test
            if boundingboxes_intersects(self.boundingbox, planet.boundingbox):
                relative_position = self.position - planet.position
                if self.collision_enabled:
                    if math.sqrt(sum(map(lambda x: x**2, relative_position))) < self.radius + planet.radius:
                        radius, degrees = self.decart2polar(relative_position)
                        radius = self.radius + planet.radius
                        self.position = planet.position + np.array(self.polar2decart((radius, degrees)))
                        self.speed *= 0.05
                planet.was_interrupted = True
                if not planet.changed_color:
                    planet.color = rgb2hex(np.fmin(np.fmax(np.array(hex2rgb(planet.color))-64, 0), 255))
                planet.changed_color = True

    # DEBUG ONLY test for rendering ball spinning in circle, pass deltatime since start of program
    # def physics(self, deltatime, radius = 200):
    #     self.position = np.array([radius * math.cos(deltatime * 0.001) + 960, radius * math.sin(deltatime * -0.001) + 540])

    def calculateAcceleration(self, decart_acceleration):
        polar = self.decart2polar(decart_acceleration)
        polar[0] = (polar[0]**(1/3))*36 # Normalize coordinates
        acceleration = self.polar2decart(polar) # Transform to decart coordinates
        self.acceleration += acceleration

    def decart2polar(self, decart):
        radius = math.sqrt(decart[0]**2 + decart[1]** 2) # Transform to polar coordinates
        degrees = math.atan2(decart[1], decart[0])
        return [radius, degrees]

    def polar2decart(self, polar):
        x = polar[0] * math.cos(polar[1])
        y = polar[0] * math.sin(polar[1])
        return [x, y]