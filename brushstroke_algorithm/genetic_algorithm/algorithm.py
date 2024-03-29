import cv2

from population import *
from brushstroke import *
from canvas import *
import time
import sys
    
"""
The algorithm is able to work only with larger images in the png file format.
PNG is required because the algorithm requires an image with a channel for transparency.
Larger images are required due to the size of the brushstroke images.
"""

if len(sys.argv) > 1:
    index = sys.argv[1].index('=')
    NUM_GENERATIONS = int(sys.argv[1][index+1:])
    #Decimal point creates new entry
    MUTATION_RATE = float(sys.argv[3])

    index = sys.argv[4].index("=")
    POP_SIZE = int(sys.argv[4][index+1:])
    
    index = sys.argv[5].index("=")
    CROSSOVER = bool(sys.argv[5][index+1:])

    index = sys.argv[6].index("=")
    IMAGE_PATH = sys.argv[6][index+1:]
else: 
    NUM_GENERATIONS = 5
    MUTATION_RATE = 0.01
    POP_SIZE = 75
    CROSSOVER = True
    IMAGE_PATH = "../static/images/sunset.png"


def main():
    im = cv2.imread(
        IMAGE_PATH, flags=cv2.IMREAD_UNCHANGED)

    population = Population(mutation_rate=MUTATION_RATE, pop_size=POP_SIZE, crossover=CROSSOVER, mutate=CROSSOVER)
    population.setup(im)

    start = time.time() # measure elapsed time
    for i in range(NUM_GENERATIONS):
        population.new_generation(population.population_size, iteration=i)
    most_fit = population.get_most_fit_individual()

    end = time.time()
    print("Elapsed time:", end - start)

    file_name = "output/result" + "-popsize" + str(POP_SIZE) + "-gens" + str(NUM_GENERATIONS)
    if population.crossover:
        file_name += "-crossover"
    if population.mutate:
        file_name += "-mut_rate" + str(MUTATION_RATE)[2:]
    file_name += ".jpeg"

    cv2.imwrite(file_name, most_fit)
    
    print("Wrote result image to", file_name)

if __name__ == "__main__":
    main()
