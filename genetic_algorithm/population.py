from individual import Individual
import numpy as np


class Population():
    def __init__(self, mutation_rate=0.01, pop_size=100):
        self.mutation_rate = mutation_rate # float, mutation rate
        self.population_size = pop_size # population size

        self.population = np.empty(pop_size, dtype=Individual) #list of Individuals
        self.mating_pool = [] #list of Individuals of those in mating pool, duplicated n times if fitness of DNA = n
        self.target_image = [] # 2d matrix -> B/W target image
        self.mating_pool_size = 0
        self.target_dims = (0, 0) # dimensions of target image: (height, width) aka (# rows, # cols)



    def setup(self, target):
        assert len(target) != 0, "target image is empty"
        self.target_image = target
        # (H, W)
        self.target_dims = (len(target), len(target[0]))
        # init individuals in the population

        # I don't think the following line works–it only initializes one individual and duplicates it
        # self.population[:self.population_size] = Individual(self.target_dims)

        for i in range(self.population_size):
            self.population[i] = Individual(self.target_dims)
        
        print(self.population.size)

    def calculate_all_fitness(self):
        for i in range(self.population_size):
            self.population[i].calculate_fitness(self.target_image) # should be an int
            # each Individual stores its own fitness

    def update_mating_pool(self):
        self.calculate_all_fitness()
        for i in range(self.population_size):
            # print("HERE!2")
            # Adds individual to mating pool number of times weighted by fitness
            for _ in range(int(self.population[i].fitness)):
            #     print("HERE!")
                self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)
        print(self.mating_pool_size)

    """
    Chooses two Individuals to reproduce.
    """
    def reproduce(self):
        fst_ind = self.mating_pool[np.random.randint(self.mating_pool_size)]
        snd_ind = self.mating_pool[np.random.randint(self.mating_pool_size)] # pick the two DNA to mate

        child = Individual(self.target_dims)
        child.crossover(fst_ind, snd_ind)
        child.mutate(self.mutation_rate)

        return child

    """
    Sorts population and removes unfit.
    """
    def fittest_survive(self):
        # sort population by fitness
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        # remove least fit
        self.population = self.population[:self.population_size]

    """
    Replace population with new generation of individuals:
    - generate new children and add to pop
    - filter out those with lowest fitness
    """
    def new_generation(self, num_children):
        self.update_mating_pool()
        new_children = np.array([self.reproduce() for _ in range(num_children)])
        self.population = np.concatenate(self.population, new_children)
        self.population = self.fittest_survive()

