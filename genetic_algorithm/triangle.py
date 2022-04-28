import numpy as np


WINDOW_WIDTH = 25
WINDOW_HEIGHT = 16

class Triangle():

    """Initialize triangle object
       If randomize, it will generate random values for the vertices. 
       Otherwise, it will use the parameters passed through
    """
    def __init__(self, x1, x2, x3, y1, y2, y3, color, randomize, size):
        if not randomize: 
            self.x1, self.y1 = x1, y1
            self.x2, self.y2 = x2, y2
            self.x3, self.y3 = x3, y3
            self.color = color
        else: 
            red = np.random.randint(255)
            green = np.random.randint(255)
            blue = np.random.randint(255)
            self.color = [red, green, blue]

            self.x1, self.y1 = self.initialize_points(size)
            self.x2, self.y2 = self.initialize_points(size)
            self.x3, self.y3 = self.initialize_points(size)

    """Randomly initialize points given size of image"""
    def initialize_points(self, size):
        x = np.random.randint(0, size[1] - 1)
        y = np.random.randint(0, size[0] - 1)
        return x,y


