import numpy as np
import random
from triangle import Triangle

class Individual():

    """
    An individual is a member of the population

    target: target image
    p1: first parent
    p2: second parent
    crossover: perform crossover of two parents
    mutate: mutate genes
    mutation_rate: rate to mutate a pixel value

    min_gene: minimum gene value
    max_gene: maximum gene value
    gene_dims: dimension of image
    gene_len: number of pixels in image #TODO: decide if needed
    genes: matrix with same dimensions as target image

    max fitness is 255^2 = 65025
    """
    def __init__(self, x1, x2, x3, y1, y2, y3, color, randomize, target, p1=None, p2=None, 
                crossover=False,mutate=False,mutation_rate=0.01):
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

            shape = np.shape(target)
            self.x1, self.y1 = self.initialize_points(shape)
            self.x2, self.y2 = self.initialize_points(shape)
            self.x3, self.y3 = self.initialize_points(shape)
        self.fitness = 0 
        self.target = target
        if crossover:
            self.crossover(p1, p2)
        if mutate:
            self.mutate(rate=mutation_rate)
        else:
            #TODO: Add something here? 
            #self.genes = np.random.randint(low=self.min_gene, high=self.max_gene, size=self.gene_dims)
            pass
        self.calculate_fitness(target)

    """Randomly initialize points given size of image"""
    def initialize_points(self, size):
        x = np.random.randint(0, size[0] - 1)
        y = np.random.randint(0, size[1] - 1)
        return x,y


    """ 
    Returns a 2D matrix of size target-dims where the location of the 
    triangle based on its vertices is colored self.color, and all other 
    values are 0 

    Template: What we are drawing on
    """
    def draw_triangle(self, target, template):
        shape = np.shape(target)

        #Right now self.genes is a 2D array, the size of the image. Each index is a 3-tuple w/ RGB 
        #self.shape is a list of Rectangle objects 
        leftmost_bound = min(self.x1, self.x2, self.x3)
        rightmost_bound = max(self.x1, self.x2, self.x3)
        bottommost_bound = min(self.y1, self.y2, self.y3)
        topmost_bound = max(self.y1, self.y2, self.y3)

        for i in range (bottommost_bound, topmost_bound):
            for j in range (leftmost_bound, rightmost_bound):
                if self.isInsideTriangle(self.x1, self.x2, self.x3, self.y1, self.y2, self.y3, i, j):
                    if i < shape[0] and j < shape[1]:
                        template[i][j] = self.color
        return template


    """
    Returns the area of a triangle given 3 points 
    """
    def area(self, x1, y1, x2, y2, x3, y3):
        return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
    
    """
    Returns whether the point P(x,y) lies within the triangle formed by 
    points (x1,y1), (x2,y2), and (x3,y3)
    """
    def isInsideTriangle(self, x1, y1, x2, y2, x3, y3, x, y):
        # Calculate area of triangle ABC
        A = self.area(x1, y1, x2, y2, x3, y3)
    
        # Calculate area of triangle PBC
        A1 = self.area(x, y, x2, y2, x3, y3)
        
        # Calculate area of triangle PAC
        A2 = self.area(x1, y1, x, y, x3, y3)
        
        # Calculate area of triangle PAB
        A3 = self.area(x1, y1, x2, y2, x, y)
        
        # Check if sum of A1, A2 and A3 is same as A
        return (A == A1 + A2 + A3)  
    
    """
    Returns int fitness of self compared to target.
    If complete opposite image (255 vs 0 for each pixel), then fitness is 0.
    If same image, fitness is 255^2.
    """
    def calculate_fitness(self, target):
        shape = np.shape(target)
        w, h = shape[0], shape[1]

        genes = self.draw_triangle(target, np.zeros((w,h,3)))

        avg_diff_squared = np.sum((genes - target)**2) / (w*h)
        self.fitness = int((255**2) - avg_diff_squared)
        # print("fitness:", self.fitness)

    """
    Changes the genes of self based on the two indivduals passed in. 
    We will be choosing a random crossover point in which we will use 
    the genes of the first individual prior to this point, and the genes
    of the second individual after this point. 

    genes: matrix with same dimensions as target image
    """
    def crossover(self, p1, p2):
        self.x1 = np.random.choice([p1.x1,p2.x1])
        self.x2 = np.random.choice([p1.x2,p2.x2])
        self.x3 = np.random.choice([p1.x3,p2.x3])

        self.y1 = np.random.choice([p1.y1,p2.y1])
        self.y2 = np.random.choice([p1.y2,p2.y2])
        self.y3 = np.random.choice([p1.y3,p2.y3])

        if np.random.randint(0,1): self.color = p1.color 
        else: self.color = p2.color
   
    """
    idea: randomly change certain pixel values
    Chooses a number of mutations based on binom distribution, num genes, and mutation rate
    """
    def mutate(self, rate):
        random_int = np.random.uniform(0,1)
        if rate < random_int:
            random_mutation = np.random.randint(0,5)
            shape = np.shape(self.target)
            w,h = shape[0], shape[1]
            if random_mutation == 0: 
                self.x1 = self.clamp(self.x1 + np.random.randint(w/5), 0, w - 1) 
                self.y1 = self.clamp(self.y1 + np.random.randint(h/5), 0, h - 1)
            elif random_mutation == 1:
                self.x2 = self.clamp(self.x2 + np.random.randint(w/5), 0, w - 1) 
                self.y2 = self.clamp(self.y2 + np.random.randint(h/5), 0, h - 1)
            elif random_mutation == 2:
                self.x3 = self.clamp(self.x3 + np.random.randint(w/5), 0, w - 1) 
                self.y3 = self.clamp(self.y3 + np.random.randint(h/5), 0, h - 1)
            elif random_mutation == 3:
                self.color[0] = self.clamp(self.color[0] + np.random.randint(255), 0, 255) 
            elif random_mutation == 4:
                self.color[1] = self.clamp(self.color[1] + np.random.randint(255), 0, 255) 
            elif random_mutation == 5:
                self.color[2] = self.clamp(self.color[2] + np.random.randint(255), 0, 255) 
            else: 
                pass 
            
    """
    Ensures that floor <= value <= ceiling
    """
    def clamp(self, value, floor, ceiling):
        if value < floor: return floor
        elif value > ceiling: return ceiling 
        return value


