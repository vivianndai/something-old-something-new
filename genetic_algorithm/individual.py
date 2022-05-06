import numpy as np
import random
from triangle import Triangle
from polygon import Polygon
import cv2

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
    def __init__(self, target, p1=None, p2=None, crossover=False, mutate=False, mutation_rate=0.01, polygons=100, vertices=3):
        self.min_gene = 0
        self.max_gene = 255 #set these values for B/W, RGBA, etc
        self.gene_dims = np.shape(target)
        self.gene_len = self.gene_dims[0] * self.gene_dims[1]
        # Genes = array that will be turned into final output image
        self.genes = np.zeros(self.gene_dims)
        # Shapes = List of triangle objects in the image 
        self.shapes = np.array([], dtype=Triangle)
        self.image_dims = np.shape(target)

        self.polygons = []
        self.num_polygons = polygons
        self.fitness = 0
        self.drawn_image = np.zeros(self.image_dims)

        if crossover and p1 and p2:
            self.crossover(p1, p2)
        if mutate:
            self.mutate(rate=mutation_rate)
        else:
            for _ in range(10):
                self.shapes = np.append(self.shapes, (Triangle(0,0,0,0,0,0,[0,0,0], True, self.gene_dims)))
            self.draw_triangles()

            # # choose a random matrix of genes (random pixel values for all genes)
            # self.polygons = np.array([Polygon(vertices, self.image_dims[:2]) for _ in range(polygons)])

        self.calculate_fitness(target)

    """ 
    For every shape in the Shape list, we will update the self.genes matrix to hold the color values that correspond
    to the shapes. 
    """
    def draw_triangles(self):
        #Right now self.genes is a 2D array, the size of the image. Each index is a 3-tuple w/ RGB 
        #self.shape is a list of Rectangle objects 
        for shape in self.shapes: 
            leftmost_bound = min(shape.x1, shape.x2, shape.x3)
            rightmost_bound = max(shape.x1, shape.x2, shape.x3)
            bottommost_bound = min(shape.y1, shape.y2, shape.y3)
            topmost_bound = max(shape.y1, shape.y2, shape.y3)

            for i in range (bottommost_bound, topmost_bound):
                for j in range (leftmost_bound, rightmost_bound):
                    if self.isInsideTriangle(shape.x1, shape.x2, shape.x3, shape.y1, shape.y2, shape.y3, i, j):
                        self.genes[i][j] = shape.color


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
    draws on canvas
    """
    def draw(self):
        for polygon in self.polygons:
            # print(polygon.vertices)
            # print(np.shape(self.drawn_image))
            cv2.fillPoly(self.drawn_image, pts=np.int32([polygon.vertices]), color=polygon.color)


    """
    Returns int fitness of self compared to target.
    If complete opposite image (255 vs 0 for each pixel), then fitness is 0.
    If same image, fitness is 255^2.
    """
    def calculate_fitness(self, target):
        # if there are non-zero entries, then the image has been drawn, no need to redraw
        if np.count_nonzero(self.drawn_image) == 0:
            self.draw()
        avg_diff_squared = np.sum((self.drawn_image - target)**2) / (self.image_dims[0] * self.image_dims[1] * 3)
        self.fitness = int((self.max_gene**2) - avg_diff_squared)
        # print("fitness:", self.fitness)

    """
    Changes the genes of self based on the two indivduals passed in. 
    We will be choosing a random crossover point in which we will use 
    the genes of the first individual prior to this point, and the genes
    of the second individual after this point. 

    genes: matrix with same dimensions as target image
    """
    def crossover(self, fst_DNA, snd_DNA):
        #Randomly choose between the two different methods listed below 
        # if (random.randint(0,1)):
        # For every entry into self.genes, randomly decide if we should use fst_DNA or snd_DNA
        choice = np.random.randint(2, size = np.shape(fst_DNA.shapes)).astype(bool)
        self.shapes = np.where(choice, fst_DNA.shapes, snd_DNA.shapes) # CHANGE: fst_DNA -> fst_DNA.genes
        # else:
            # Picks a random row to use first_DNA genes, then uses snd_DNA genes for the rest of the rows
            # random_row = np.random.randint(fst_DNA.genes.shape[0])
            # self.genes = fst_DNA.genes[:random_row]
            # self.genes = np.append(self.genes, np.array(snd_DNA.genes[random_row:]), axis = 0)

    """
    Crossover between two triangle objects
    """
    def crossover_triangle(self, tri1, tri2):
        x1 = np.random.choice([tri1.x1,tri2.x1])
        x2 = np.random.choice([tri1.x2,tri2.x2])
        x3 = np.random.choice([tri1.x3,tri2.x3])

        y1 = np.random.choice([tri1.y1,tri2.y1])
        y2 = np.random.choice([tri1.y2,tri2.y2])
        y3 = np.random.choice([tri1.y3,tri2.y3])

        color = np.random.choice([tri1.color,tri2.color])
        return Triangle(x1,x2,x3,y1,y2,y3,color,False, self.gene_dims)
   
    """
    idea: randomly pick a set of polygons to mutate
    Chooses a number of mutations based on binom distribution, num genes, and mutation rate
    """
    def mutate(self, rate):
        n_mutations = np.random.binomial(self.gene_len, rate)
        for _ in range(n_mutations):
            random_index = np.random.randint(0, np.shape(self.shapes))
            random_triangle = self.shapes[random_index]
            self.mutate_triangle(random_triangle[0])
            # self.shapes[random_index] = self.mutate_triangle(random_triangle)
        
        # mutation_list = np.random.binomial(1, rate, size=self.num_polygons).astype(bool)
        # for i in range(self.num_polygons):
        #     if mutation_list[i]:
        #         self.polygons[i].mutate_points(i)
        # # if anything mutated, redraw
        # if np.count_nonzero(mutation_list) != 0:
        #     self.draw()

    """
    Mutation of a triangle object
    """
    def mutate_triangle(self, triangle):
        random_mutation = np.random.randint(9)
        if random_mutation == 0: 
            triangle.x1 = self.clamp(triangle.x1 + np.random.randint(self.gene_dims[0]/5), 0, self.gene_dims[0] - 1) 
            triangle.y1 = self.clamp(triangle.y1 + np.random.randint(self.gene_dims[1]/5), 0, self.gene_dims[1] - 1)
        elif random_mutation == 1:
            triangle.x2 = self.clamp(triangle.x2 + np.random.randint(self.gene_dims[0]/5), 0, self.gene_dims[0] - 1) 
            triangle.y2 = self.clamp(triangle.y2 + np.random.randint(self.gene_dims[1]/5), 0, self.gene_dims[1] - 1)
        elif random_mutation == 2:
            triangle.x3 = self.clamp(triangle.x3 + np.random.randint(self.gene_dims[0]/5), 0, self.gene_dims[0] - 1) 
            triangle.y3 = self.clamp(triangle.y3 + np.random.randint(self.gene_dims[1]/5), 0, self.gene_dims[1] - 1)
        elif random_mutation == 3:
            triangle.color[0] = np.random.randint(255)
            triangle.color[1] = np.random.randint(255)
            triangle.color[2] = np.random.randint(255)

        # elif random_mutation == 4:
        # elif random_mutation == 5:
        else: 
            pass 

    """
    Ensures that floor <= value <= ceiling
    """
    def clamp(self, value, floor, ceiling):
        if value < floor: return floor
        elif value > ceiling: return ceiling 
        return value


    """
    Normalizes fitness to be between 0 and 1.
    Returns: x: float, 0 <= x <= 1
    """
    def normalize_fitness(self):
        return self.fitness/255**2
