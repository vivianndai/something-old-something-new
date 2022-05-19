import numpy as np
import random
import cv2
from brushstroke import Brushstroke
from canvas import Canvas


class Population():
    def __init__(self, mutation_rate=0.01, pop_size=100, crossover=True, mutate=True):
        self.mutation_rate = mutation_rate
        self.population_size = pop_size
        self.population = np.empty(pop_size, dtype=Canvas)
        self.mating_pool = []
        self.mating_pool_size = 0
        self.target_image = []
        self.target_dims = (0, 0)
        self.copies_in_mating_pool = 100
        self.crossover = crossover
        self.mutate = mutate

    def setup(self, target):
        assert len(target) != 0, "target image is empty"
        self.target_image = target
        self.target_dims = (target.shape[0], target.shape[1])
        canvas = Canvas(self.target_image)
        for i in range(self.population_size):
            self.population[i] = canvas.generate_random_canvas()

    def calculate_all_fitness(self):
        for i in range(self.population_size):
            self.population[i].calculate_fitness(
                self.target_image)  # should be an int
            # each Canvas stores its own fitness

    def update_mating_pool(self, iteration):
        print("--------------------------------------------- Generation",
              iteration, "---------------------------------------------")
        if iteration != 0:
            self.calculate_all_fitness()
        for i in range(self.population_size):
            num_adding_to_pool = int(
                self.population[i].fitness / 255**2 * self.copies_in_mating_pool)
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
        child = []
        for i in range(25):
            x = random.randint(0, 50)
            child.append(parent_1[x], parent_2[x])
        return child

    """
    Sorts population and removes unfit.
    """

    def fittest_survive(self, children):
        # sort population by fitness
        self.population = sorted(
            self.population, key=lambda x: x.fitness, reverse=True)
        # remove least fit
        self.population = self.population[:self.population_size]
        print("Best individuals in generation:", [
              int(i.fitness / 255**2 * 10**4) / 10**2 for i in self.population])

    """
    Replace population with new generation of individuals:
    - generate new children and add to pop
    - filter out those with lowest fitness
    """

    def new_generation(self, num_children, iteration):
        self.update_mating_pool(iteration)
        new_children = np.array([self.reproduce()
                                 for _ in range(num_children)])
        self.population = np.concatenate((self.population, new_children))
        self.fittest_survive(new_children)

    def get_most_fit_individual(self):
        return self.population[0].drawn_image
