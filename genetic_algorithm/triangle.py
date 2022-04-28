import numpy as np


WINDOW_WIDTH = 25
WINDOW_HEIGHT = 16
#TODO: change this to be dependent on screen width/height
MAX_MOVEMENT = 5
MAX_SCALE = 2
#TODO: change this based on visual testing 
MAX_SIZE = 10
MIN_SIZE = 2

class Triangle():

    def __init__(self, x1, x2, x3, y1, y2, y3, color, randomize):
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

            self.x1, self.y1 = self.initialize_points()
            self.x2, self.y2 = self.initialize_points()
            self.x3, self.y3 = self.initialize_points()

    def initialize_points(self):
        x = np.random.randint(0, WINDOW_WIDTH - 1)
        y = np.random.randint(0, WINDOW_HEIGHT - 1)
        return x,y


    def get_x1(self):
        return self.x1




