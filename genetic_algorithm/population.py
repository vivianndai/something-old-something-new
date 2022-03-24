from individual import Individual
import numpy as np

# need to replace the loops with more efficient numpy methods for matrices

class Population():
    def __init__(self, mutation_rate, pop):
        self.mutation_rate = mutation_rate # float, mutation rate
        self.population_size = pop # population size

        self.population = [] #list of Individuals
        self.mating_pool = [] #list of Individuals of those in mating pool, duplicated n times if fitness of DNA = n
        self.target_image = [] # 2d matrix -> B/W target image
        self.mating_pool_size = 0
        self.target_dims = (0, 0) # dimensions of target image: (height, width) aka (# rows, # cols)


    def setup(self, target):
        self.target_image = target
        self.target_len = 0
        # init individuals in the population
        self.population = np.array([Individual() for _ in range(self.population_size)])
    
    def calculate_all_fitness(self):
        for i in range(self.population_size):
            self.population[i].fitness(self.target_image) # should be an int
            # each Individual stores its own fitness

    def update_mating_pool(self):
        for i in range(self.population_size):
            for j in range(self.fitness[i]):
                self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)

    """
    Chooses two Individuals to reproduce.
    """
    def reproduce(self):
        fst_ind = self.mating_pool[np.random.randint(self.mating_pool_size)]
        snd_ind = self.mating_pool[np.random.randint(self.mating_pool_size)] # pick the two DNA to mate

        child = Individual(self.target_len)
        child.crossover(fst_ind, snd_ind)
        child.mutate(self.mutation_rate)

        return child

    """
    Sorts population and removes unfit.
    """
    def fittest_survive(self):
        # Sort by fitness here? is this inefficient? how large of a population is realistic?
        # ----- sort population ------

        # remove least fit
        self.population = self.population[:self.population_size]

    """
    Replace population with new generation of individuals:
    - generate new children and add to pop
    - filter out those with lowest fitness
    """
    def new_generation(self, num_children):
        new_children = np.array([self.reproduce() for _ in range(num_children)])
        self.population = np.concatenate(self.population, new_children)

        self.population = self.fittest_survive()

