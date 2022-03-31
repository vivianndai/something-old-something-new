from individual import Individual
import numpy as np

# TODO:
# - document all functions
# - have some way of keeping track what is being worked on, what are TODOs at this scale

# code TODO:
# - decide what goes in init vs setup
# - conversion to RGB needs to be all at once, or else some things will break


class Population():
    """
    mutation rate (float): rate at which we randomly mutate an element of the image during reproduction
    population_size (int): number of images in our total population
    population (Individual list): list of [population_size] Individuals (images)
    mating_pool (Individual list): each element of mating_pool is in the population.
                 - they are duplicated a number of times in the mating_pool based on their fitness.
    mating_pool_size (int): the number of individuals in the mating pool
    target_image (pixel matrix): the image we want to recreate in matrix representation
    target_dims (int, int): dimensions of the target image (# rows, #cols)
    total_fitness (int): sum of all of the fitness values of Individuals
                         - needed to make proportionate mating pool
    """
    def __init__(self, mutation_rate=0.01, pop_size=100):
        self.mutation_rate = mutation_rate
        self.population_size = pop_size
        self.population = np.empty(pop_size) # CHANGE: we don't need , dtype=Individual) here.
        self.mating_pool = []
        self.mating_pool_size = 0
        self.target_image = []
        self.target_dims = (0, 0)
        self.total_fitness = 0 


    """
    Given a target image, initializes a new population.
    """
    def setup(self, target):
        assert len(target) != 0, "target image is empty"
        self.target_image = target
        self.target_dims = (len(target), len(target[0]))

        # I don't think the following line works–it only initializes one individual and duplicates it
        # self.population[:self.population_size] = Individual(self.target_dims)

        for i in range(self.population_size):
            self.population[i] = Individual(self.target_image)

    def calculate_all_fitness(self):
        # TODO: optimization: only calculate fitness for new children
        self.total_fitness = 0
        for i in range(self.population_size):
            self.population[i].calculate_fitness(self.target_image) # should be an int
            # each Individual stores its own fitness
            self.total_fitness += self.population[i].fitness

    def update_mating_pool(self, iteration):
        # TODO: Vivian will work on this method
        if iteration != 0:
            self.calculate_all_fitness()
        for i in range(self.population_size): 
            for _ in range(int(self.population[i].fitness)):
                self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)
        print(self.mating_pool_size)


    """
    Chooses two Individuals to reproduce at random from the mating pool.
    Initializes new child, performs crossover and mutation.
    """
    def reproduce(self):
        parent_1 = self.mating_pool[np.random.randint(self.mating_pool_size)]
        parent_2 = self.mating_pool[np.random.randint(self.mating_pool_size)]

        child = Individual(self.target_dims, p1 = parent_1, p2 = parent_2, crossover=True, mutate=True, mutation_rate=self.mutation_rate)

        return child

    """
    Sorts population and removes unfit.
    """
    def fittest_survive(self, children):
        # sort population by fitness
        self.population = sorted(self.population, key=lambda x: x.fitness, reverse=True)
        # remove least fit
        self.population = self.population[:self.population_size]

    """
    Replace population with new generation of individuals:
    - generate new children and add to pop
    - filter out those with lowest fitness
    """
    def new_generation(self, num_children, iteration):
        self.update_mating_pool(iteration)
        new_children = np.array([self.reproduce() for _ in range(num_children)])
        self.population = np.concatenate(self.population, new_children)
        self.population = self.fittest_survive(new_children)

