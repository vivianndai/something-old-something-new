import numpy as np

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

        self.fitness = self.calculate_fitness(target)

    """
    Returns int fitness of self compared to target.
    If complete opposite image (255 vs 0 for each pixel), then fitness is 0.
    If same image, fitness is 255^2.
    """
    def calculate_fitness(self, target):
        avg_diff_squared = np.sum((self.genes - target)**2) / self.gene_len
        self.fitness = int((self.max_gene**2) - avg_diff_squared)
        print("fitness is %f", self.fitness)


    """
    #TODO: rewrite this and the method
    """
    def crossover(self, fst_DNA, snd_DNA):
        crossover_point = np.random.randint(self.gene_len)
        self.genes[:crossover_point] = fst_DNA.genes[:crossover_point]
        self.genes[crossover_point:] = snd_DNA.genes[crossover_point:]


    """
    idea: randomly change certain pixel values
    Chooses a number of mutations based on binom distribution, num genes, and mutation rate
    """
    #TODO: need to fix this, inconsistent RGB vs B/W
    def mutate(self, rate):
        n_mutations = np.random.binomial(self.gene_len, rate)
        self.genes[np.random.randint(0, self.gene_dims[0], size=n_mutations)][np.random.randint(0, self.gene_dims[1], size=n_mutations)] = np.random.randint(self.min_gene, self.max_gene, size = 3)
