import numpy as np

class DNA():

    def __init__(self, target_len):
        self.min_gene = 0
        self.max_gene = 255 #set these values for B/W, RGB, etc
        self.gene_len = target_len
        self.genes = [np.random.randint(self.min_gene, self.max_gene) for _ in range(target_len)]
        self.fitness = 0 # float fitness

    def fitness(self, target):
        # return int fitness of self compared to target
        self.fitness = np.sum(self.genes == target) / self.gene_len


    def crossover(self, fst_DNA, snd_DNA):
        # idea: crossover is unlikely to generate the right image because there are 255 int values
        # that pixels can take (vs 26 for letters in words)
        # have our fitness measure take closeness into account
        crossover_point = np.random.randint(self.gene_len)
        self.genes[:crossover_point] = fst_DNA.genes[:crossover_point]
        self.genes[crossover_point:] = snd_DNA.genes[crossover_point:]


    def mutate(self, rate):
        pass