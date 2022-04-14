import numpy as np
import random

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
    def __init__(self, target, p1=None, p2=None, crossover=False, mutate=False, mutation_rate=0.01):
        self.min_gene = 0
        self.max_gene = 255 #set these values for B/W, RGBA, etc
        self.gene_dims = np.shape(target)
        self.gene_len = self.gene_dims[0] * self.gene_dims[1]
        self.genes = np.zeros(self.gene_dims)

        if crossover:
            self.crossover(p1, p2)
        if mutate:
            self.mutate(rate=mutation_rate)
        else:
            # choose a random matrix of genes (random pixel values for all genes)
            self.genes = np.random.randint(low=self.min_gene, high=self.max_gene, size=self.gene_dims)

        self.calculate_fitness(target)

    """
    Returns int fitness of self compared to target.
    If complete opposite image (255 vs 0 for each pixel), then fitness is 0.
    If same image, fitness is 255^2.
    """
    def calculate_fitness(self, target):
        avg_diff_squared = np.sum((self.genes - target)**2) / self.gene_len
        self.fitness = int((self.max_gene**2) - avg_diff_squared)
        print("fitness:", self.fitness)


    """
    Changes the genes of self based on the two indivduals passed in. 
    We will be choosing a random crossover point in which we will use 
    the genes of the first individual prior to this point, and the genes
    of the second individual after this point. 

    genes: matrix with same dimensions as target image
    """
    def crossover(self, fst_DNA, snd_DNA):
        #Randomly choose between the two different methods listed below 
        if (random.randint(0,1)):
        # For every entry into self.genes, randomly decide if we should use fst_DNA or snd_DNA
            choice = np.random.randint(2, size = fst_DNA.genes.size).reshape(fst_DNA.genes.shape).astype(bool)
            self.genes = np.where(choice, fst_DNA.genes, snd_DNA.genes) # CHANGE: fst_DNA -> fst_DNA.genes
        else:
            # Picks a random row to use first_DNA genes, then uses snd_DNA genes for the rest of the rows
            random_row = np.random.randint(fst_DNA.genes.shape[0])
            self.genes = fst_DNA.genes[:random_row]
            self.genes = np.append(self.genes, np.array(snd_DNA.genes[random_row:]), axis = 0)




    """
    idea: randomly change certain pixel values
    Chooses a number of mutations based on binom distribution, num genes, and mutation rate
    """
    def mutate(self, rate):
        pixel_value = self.genes[0][0].size
        n_mutations = np.random.binomial(self.gene_len, rate)
        for _ in range(n_mutations):
            random_row = np.random.randint(0, self.gene_dims[0])
            random_col = np.random.randint(0, self.gene_dims[1])
            random_value = np.random.randint(self.min_gene, self.max_gene, size = pixel_value)
            self.genes[random_row][random_col] = random_value
