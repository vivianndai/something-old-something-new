from individual import Individual
import numpy as np

# need to replace the loops with more efficient numpy methods for matrices

class Population():
    def __init__(self, mutation_rate, pop):
        self.mutation_rate = mutation_rate # float, mutation rate
        self.population_size = pop # population size

        self.population = np.empty(pop, dtype=Individual) #list of Individuals
        self.mating_pool = [] #list of Individuals of those in mating pool, duplicated n times if fitness of DNA = n
        self.target_image = [] # 2d matrix -> B/W target image
        self.mating_pool_size = 0
        self.target_dims = (0, 0) # dimensions of target image: (height, width) aka (# rows, # cols)



    def setup(self, target):
        assert len(target) != 0, "target image is empty"
        self.target_image = target

        # (H, W)
        self.target_dims = (len(target), len(target[0]))
        print(self.target_dims)
        # init individuals in the population
        #CHANGED TO NUMPY 
        self.population[:self.population_size] = Individual(self.target_dims)
        # for i in range(self.population_size):
        #     self.population[i] = Individual(self.target_dims)
        
        print(self.population.size)

    def calculate_all_fitness(self):
        for i in range(self.population_size):
            self.population[i].calculate_fitness(self.target_image) # should be an int
            # each Individual stores its own fitness

    def update_mating_pool(self):
        self.calculate_all_fitness()
        for i in range(self.population_size):
            # print("HERE!2")
            # print(str(int(self.population[i].fitness)))
            # for _ in range(int(self.population[i].fitness)):
            #     print("HERE!")
            self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)
        print(self.mating_pool_size)

    """
    Chooses two Individuals to reproduce.
    """
    def reproduce(self):
        self.update_mating_pool()

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

