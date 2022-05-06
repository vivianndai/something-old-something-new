import numpy as np


WINDOW_WIDTH = 25
WINDOW_HEIGHT = 16

class Polygon():

    """Initialize polygon object
        color: [R, G, B]
        vertices: [(x, y), ...]
    """
    def __init__(self, num_vertices, img_size):
        self.num_vertices = num_vertices
        self.img_size = img_size

        self.color = self.initialize_color()
        self.vertices = np.array([self.initialize_points() for _ in range(num_vertices)])

    """Randomly initialize points given size of image"""
    def initialize_points(self):
        # x = np.random.randint(0, self.img_size[1] - 1)
        # y = np.random.randint(0, self.img_size[0] - 1)
        x = np.random.uniform()
        y = np.random.uniform()

        return [x, y]

    def initialize_color(self):
        red = np.random.randint(255)
        green = np.random.randint(255)
        blue = np.random.randint(255)
        
        return [red, green, blue]
    
    def mutate_points(self):
        self.vertices = np.array([self.initialize_points() for _ in range(self.num_vertices)])
        self.color = self.initialize_color()