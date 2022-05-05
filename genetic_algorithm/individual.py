import numpy as np
import random
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
            # choose a random matrix of genes (random pixel values for all genes)
            self.polygons = np.array([Polygon(vertices, self.image_dims[:2]) for _ in range(polygons)])

        self.calculate_fitness(target)

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
        choice = np.random.binomial(1, fst_DNA.normalize_fitness(), size=self.num_polygons).astype(bool)
        self.polygons = np.where(choice, fst_DNA.polygons, snd_DNA.polygons) # CHANGE: fst_DNA -> fst_DNA.genes
        # else:
            # Picks a random row to use first_DNA genes, then uses snd_DNA genes for the rest of the rows
            # random_row = np.random.randint(fst_DNA.genes.shape[0])
            # self.genes = fst_DNA.genes[:random_row]
            # self.genes = np.append(self.genes, np.array(snd_DNA.genes[random_row:]), axis = 0)


    """
    idea: randomly pick a set of polygons to mutate
    Chooses a number of mutations based on binom distribution, num genes, and mutation rate
    """
    def mutate(self, rate):
        mutation_list = np.random.binomial(1, rate, size=self.num_polygons).astype(bool)
        for i in range(self.num_polygons):
            if mutation_list[i]:
                self.polygons[i].mutate_points(i)
        # if anything mutated, redraw
        if np.count_nonzero(mutation_list) != 0:
            self.draw()

    """
    Normalizes fitness to be between 0 and 1.
    Returns: x: float, 0 <= x <= 1
    """
    def normalize_fitness(self):
        return self.fitness/255**2