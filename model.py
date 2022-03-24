from dna import DNA
import numpy as np
from rectangle import Rectangle

# need to replace the loops with more efficient numpy methods for matrices

class Algorithm():
    def __init__(self, mutation_rate, pop):
        self.mutation_rate = mutation_rate # float, mutation rate
        self.total_population = pop # population size

        self.population = [0 * pop] #list of DNA
        self.mating_pool = [] #list of DNA of those in mating pool, duplicated n times if fitness of DNA = n
        self.target_image = [] # 2d matrix -> B/W target image
        self.mating_pool_size = 0
        self.target_len = 0

    def setup(self, target):
        self.target_image = target
        self.target_len = 0

        for i in range(self.total_population):
            # self.total_population[i] = DNA(len(target))
            self.total_population[i] = Rectangle()

    
    def calculate_fitness(self):
        for i in range(self.total_population):
            self.population[i].fitness(self.target_image) # should be an int
            # each DNA stores its own fitness

    #Don't have fitness for every rectangle....have a fitness for the image with the 
    #new rectangle on it (i think)
    #TODO: Change to NP arrays 
    #TODO: Figure out the type of this "image"
    def calculate_image_fitness(self, image1, image2):
        error = 0 
        for r in range(image1[0]):
            for c in range(r[0]):
                rgb1 = image1[r][c]
                rgb2 = image2[r][c]

                red_error = np.sqrt(rgb1[0]**2 + rgb2[0]**2)
                green_error = np.sqrt(rgb1[1]**2 + rgb2[0]**2)
                blue_error = np.sqrt(rgb1[2]**2 + rgb2[0]**2)

                error += red_error + green_error + blue_error

        return error
                

    def update_mating_pool(self):
        for i in range(self.total_population):
            for j in range(self.fitness[i]):
                self.mating_pool.append(self.population[i])
        self.mating_pool_size = len(self.mating_pool)

        """
        Chooses two DNA to reproduce.
        """
    def reproduce(self):
        fst_DNA = self.mating_pool[np.random.randint(self.mating_pool_size)]
        snd_DNA = self.mating_pool[np.random.randint(self.mating_pool_size)] # pick the two DNA to mate


        # child = DNA(self.target_len)
        child = Rectangle()
        #Constructor randomly assigns values, crossover overwrites this -> place for efficiency updates
        child.crossover(fst_DNA, snd_DNA)
        child.mutate(self.mutation_rate)

        # add child to new population???
