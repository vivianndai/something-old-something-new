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
    copies_in_mating_pool (int): the number of times an individual with perfect fitness is added to the mating pool
                         - needed to make proportionate mating pool
                         - e.g if fitness = 255^2 = MAX_FITNESS, then added [copies_in_mating_pool] times
                         - if fitness is half of that, added half the number of times, etc.
    """
    def __init__(self, mutation_rate=0.01, pop_size=100):
        self.mutation_rate = mutation_rate
        self.population_size = pop_size
        self.population = np.empty(pop_size, dtype = Individual) # CHANGE: added dtype=Individual) here because I got an error
        self.mating_pool = []
        self.mating_pool_size = 0
        self.target_image = []
        self.target_dims = (0, 0)
        self.copies_in_mating_pool = 100


    """
    Given a target image, initializes a new population.
    """
    def setup(self, target):
        assert len(target) != 0, "target image is empty"
        self.target_image = target
        self.target_dims = (len(target), len(target[0]))

        for i in range(self.population_size):
            self.population[i] = Individual(self.target_image)

    def calculate_all_fitness(self):
        for i in range(self.population_size):
            self.population[i].calculate_fitness(self.target_image) # should be an int
            # each Individual stores its own fitness

    def update_mating_pool(self, iteration):
        print("--------------------------------------------- Generation", iteration, "---------------------------------------------")
        if iteration != 0:
            self.calculate_all_fitness()
        for i in range(self.population_size): 
            num_adding_to_pool = int(self.population[i].fitness / 255**2 * self.copies_in_mating_pool)
            for _ in range(num_adding_to_pool):
                self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)

    """
    Chooses two Individuals to reproduce at random from the mating pool.
    Initializes new child, performs crossover and mutation.
    """
    def reproduce(self):
        parent_1 = self.mating_pool[np.random.randint(self.mating_pool_size)]
        parent_2 = self.mating_pool[np.random.randint(self.mating_pool_size)]

        child = Individual(target=self.target_image, p1=parent_1, p2=parent_2, crossover=True, mutate=True, mutation_rate=self.mutation_rate)

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
        self.population = np.concatenate((self.population, new_children))
        self.fittest_survive(new_children)

