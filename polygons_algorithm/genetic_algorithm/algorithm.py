# Runs the algorithm
import cv2
from population import Population 
import time
import sys

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
    POLYGONS = int(sys.argv[6][index+1:])

    index = sys.argv[7].index("=")
    VERTICES = int(sys.argv[7][index+1:])

    index = sys.argv[8].index("=")
    IMAGE_PATH = sys.argv[8][index+1:]
else: 
    NUM_GENERATIONS = 350
    MUTATION_RATE = 0.05
    POP_SIZE = 75
    CROSSOVER = True
    POLYGONS = 200
    VERTICES = 3
    IMAGE_PATH = "../static/images/small.jpeg"


def main():
    im = cv2.imread(IMAGE_PATH, flags=cv2.IMREAD_COLOR)    

    population = Population(mutation_rate=MUTATION_RATE, pop_size=POP_SIZE, crossover=CROSSOVER, mutate=CROSSOVER, polygons=POLYGONS, vertices=VERTICES)
    population.setup(im)

    start = time.time() # measure elapsed time
    for i in range(NUM_GENERATIONS):
        population.new_generation(population.population_size, iteration=i)

    end = time.time()
    
    most_fit = population.get_most_fit_individual()
    file_name = "output/result" + "-popsize" + str(POP_SIZE) + "-gens" + str(NUM_GENERATIONS)
    if population.crossover:
        file_name += "-crossover"
    if population.mutate:
        file_name += "-mut_rate" + str(MUTATION_RATE)[2:]
    file_name += ".jpeg"

    cv2.imwrite(file_name, most_fit)
    print("Elapsed time:", end - start)
    
    print("Wrote result image to", file_name)

if __name__ == "__main__":
    main()




# # Runs the algorithm
# import numpy as np
# # from PIL import Image
# import cv2
# from population import Population 
# import time
# import numpy as np

# NUM_GENERATIONS = 300
# MUTATION_RATE = 0.01
# POP_SIZE = 50
# CROSSOVER = True
# POLYGONS = 125
# VERTICES = 4


# def main():
#     im = cv2.imread("../static/images/frog.jpeg",flags=cv2.IMREAD_COLOR)    

#     population = Population(mutation_rate=MUTATION_RATE, pop_size=POP_SIZE, crossover=CROSSOVER, mutate=CROSSOVER, polygons=POLYGONS, vertices=VERTICES)
#     population.setup(im)

#     start = time.time() # measure elapsed time
#     for i in range(NUM_GENERATIONS):
#         population.new_generation(population.population_size, iteration=i)
#     most_fit = population.get_most_fit_individual()

#     end = time.time()
#     print("Elapsed time:", end - start)

#     file_name = "output/result" + "-popsize" + str(POP_SIZE) + "-gens" + str(NUM_GENERATIONS)
#     if population.crossover:
#         file_name += "-crossover"
#     if population.mutate:
#         file_name += "-mut_rate" + str(MUTATION_RATE)[2:]
#     file_name += ".jpeg"

#     cv2.imwrite(file_name, most_fit)
    
#     print("Wrote result image to", file_name)

# if __name__ == "__main__":
#     main()