from random import choice, randint
from defaults import *

class Planet:
    def __init__(self, colors=default_colors) -> None:
        self.color = choice(colors)
        self.position = (randint(planet_offset, screen_size[0]-planet_offset), randint(planet_offset, screen_size[1]-planet_offset))
        self.radius = randint(15, 50)
        self.mass = (self.radius * 1)**2
        self.boundingbox_coordinates = ((self.position[0] - self.radius, self.position[1] - self.radius), (self.position[0] + self.radius, self.position[1] + self.radius))
        self.boundingbox = {
            "left": self.position[0] - self.radius,
            "right": self.position[0] + self.radius,
            "top": self.position[1] - self.radius,
            "down": self.position[1] + self.radius,
        }
        self.was_interrupted = True
        self.changed_color = False