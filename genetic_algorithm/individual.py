import numpy as np

class Individual():

    """
    An individual is a member of the population

    target_dims: (height, width) of the target image
    """
    def __init__(self, target_dims):
        self.min_gene = 0
        self.max_gene = 255 #set these values for B/W, RGBA, etc
        self.gene_dims = target_dims
        self.gene_len = target_dims[0] * target_dims[1]

        # choose a random seq of genes (random pixel values for all genes)
        self.genes = np.array([[np.random.randint(self.min_gene, self.max_gene, size = 3) for _ in range(target_dims[1])] for _ in range(target_dims[0])])
        self.fitness = 0.0 # float fitness

    def calculate_fitness(self, target):
        # return int fitness of self compared to target
        # this is the sum of the squared differences between all pixel values
        # normalized by dividing by the size of the image (is this necessary?)

        diff_squared = np.sum((self.genes - target)**2) 
        self.fitness = 1 - diff_squared / (self.max_gene**2)


    def crossover(self, fst_DNA, snd_DNA):
        # idea: crossover is unlikely to generate the right image because there are 255 int values
        # that pixels can take (vs 26 for letters in words)
        # have our fitness measure take closeness into account
        crossover_point = np.random.randint(self.gene_len)
        self.genes[:crossover_point] = fst_DNA.genes[:crossover_point]
        self.genes[crossover_point:] = snd_DNA.genes[crossover_point:]


    def mutate(self, rate):
        # idea: randomly change certain pixel values
        # chooses a number of mutations based on binom distribution, num genes, and mutation rate
        n_mutations = np.random.binomial(self.gene_len, rate)
        # changes that number of selected indices to random gene value
        # print('GENE LENGTH: ' + str(self.gene_len))
        self.genes[np.random.randint(0, self.gene_dims[0], size=n_mutations)][np.random.randint(0, self.gene_dims[1], size=n_mutations)] = np.random.randint(self.min_gene, self.max_gene, size = 3)
