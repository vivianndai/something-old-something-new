import numpy as np
import random
import cv2

from population import *
from brushstroke import *
from canvas import *
import time

NUM_GENERATIONS = 300
MUTATION_RATE = 0.05
POP_SIZE = 50
CROSSOVER = False
IMAGE_PATH = "../static/images/small.jpeg"

"""
only works with pngs
of a certain size
etc.
"""


def main():

    im = cv2.imread(
        IMAGE_PATH, flags=cv2.IMREAD_UNCHANGED)

    population = Population(mutation_rate=MUTATION_RATE, pop_size=POP_SIZE,
                            crossover=CROSSOVER, mutate=CROSSOVER)
    population.setup(im)

    start = time.time()  # measure elapsed time
    for i in range(NUM_GENERATIONS):
        population.new_generation(population.population_size, iteration=i)
        most_fit = population.get_most_fit_individual()
        file_name = "output/result" + "-popsize" + \
            str(POP_SIZE) + "-gens" + str(NUM_GENERATIONS)
        if population.crossover:
            file_name += "-crossover"
        if population.mutate:
            file_name += "-mut_rate" + str(MUTATION_RATE)[2:]
        file_name += ".jpeg"

        cv2.imwrite(file_name, most_fit)

    end = time.time()

    print("Elapsed time:", end - start)

    print("Wrote result image to", file_name)


if __name__ == "__main__":
    main()
