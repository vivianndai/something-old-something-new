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

        self.center = self.initialize_points()

        self.color = self.initialize_color()
        self.vertices = self.initialize_vertices()

    """Randomly initialize points given size of image"""
    def initialize_points(self):
        x = np.random.random()
        y = np.random.random()

        return [x, y]

    """
    Initializes array of vertices in the range [-0.5, 1.5). Will be scaled up to the canvas in draw.
    """
    def initialize_vertices(self):
        x, y = self.center
        return np.array([[x + np.random.random() - 0.5, y + np.random.random() - 0.5] for _ in range(self.num_vertices)])

    def initialize_color(self):
        red = np.random.randint(255)
        green = np.random.randint(255)
        blue = np.random.randint(255)
        
        return [red, green, blue]
    
    def mutate_points(self):
        
        new_vertices = np.array([self.mutate_vertex(v) for v in self.vertices])
        self.vertices = new_vertices
        # self.color = self.initialize_color()

        # dna += Math.random() * mutateAmount * 2 - mutateAmount;
        # Red = 150, want to add small change to color [-delta,+delta]
        self.color = self.mutate_color(self.color)


    def mutate_vertex(self, v):
        return [v[0] + np.random.random() * 0.1 * 2 - 0.1, v[1] + np.random.random() * 0.1 * 2 - 0.1]

    def mutate_color(self, color):
        return [int(c + np.random.random() * 0.1 * 2 - 0.1) for c in color]