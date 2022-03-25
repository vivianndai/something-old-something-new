import numpy as np


WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
#Change this based on whether we have RGB or some other color system 
MAX_COLOR = 100
#TODO: change this to be dependent on screen width/height
MAX_MOVEMENT = 200
MAX_SCALE = 10
#TODO: change this based on visual testing 
MAX_SIZE = 200
MIN_SIZE = 10

class Rectangle():

    #No arguments because everything is randomized at the start of the generation
    def __init__(self):
        red = np.random.randint(255)
        green = np.random.randint(255)
        blue = np.random.randint(255)
        self.color = [red, green, blue]

        self.width = np.random.randint(MIN_SIZE, MAX_SIZE)
        self.height = np.random.randint(MIN_SIZE, MAX_SIZE)

        self.x = np.random.randint(0, WINDOW_WIDTH - self.width)
        self.y = np.random.randint(0, WINDOW_HEIGHT - self.height)
        self.z = np.random.randint(200) 

    def __init__(self, color, x, y, z, width, height):
        self.color = color
        self.x = x 
        self.y = y
        self.z = z
        self.width = width
        self.height = height

    def draw_rectangle(self):
        pass 

    def get_max_mvmt_change(self):
        return MAX_MOVEMENT

    def get_max_color_change(self):
        return MAX_COLOR

    def clamp(self, value, floor, ceiling):
        if value < floor: return floor
        elif value > ceiling: return ceiling 
        return value

    def crossover_rectangle(self, rect1, rect2):
        self.x = np.random.choice([rect1.x,rect2.x])
        self.y = np.random.choice([rect1.y,rect2.y])
        self.z = np.random.choice([rect1.z,rect2.z])
        self.width = np.random.choice([rect1.width,rect2.width])
        self.height = np.random.choice([rect1.height,rect2.height])
        self.color = np.random.choice([rect1.color,rect2.color])

    def mutate_rectangle(self, rectangle):
        random_mutation = np.random.randint(9)
        if random_mutation == 0: 
            rectangle.x = self.clamp(rectangle.x + np.random.randint(MAX_MOVEMENT), 0, WINDOW_WIDTH - rectangle.width) 
        elif random_mutation == 1:
            rectangle.y = self.clamp(rectangle.y + np.random.randint(MAX_MOVEMENT), 0, WINDOW_HEIGHT - rectangle.height)
        elif random_mutation == 2:
            #Moves rectangle closer / further away
            rectangle.z = np.random.randint(200) 
        elif random_mutation == 3:
            rectangle.width = self.clamp(rectangle.width + np.random.randint(MAX_SCALE), MIN_SIZE, WINDOW_WIDTH) 
        elif random_mutation == 4:
            rectangle.height = self.clamp(rectangle.height + np.random.randint(MAX_SCALE), MIN_SIZE, WINDOW_HEIGHT) 
        elif random_mutation == 5:
            rectangle.color[0] = self.clamp(rectangle.color[0] + np.random.randint(MAX_COLOR), 0, 255) 
        elif random_mutation == 6:
            rectangle.color[1] = self.clamp(rectangle.color[1] + np.random.randint(MAX_COLOR), 0, 255) 
        elif random_mutation == 7:
            rectangle.color[2] = self.clamp(rectangle.color[2] + np.random.randint(MAX_COLOR), 0, 255) 
        else: 
            pass 

