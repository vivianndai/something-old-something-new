# Runs the algorithm
import numpy as np
# from PIL import Image
import cv2
from population import Population 
import time
import numpy as np

NUM_GENERATIONS = 20
MUTATION_RATE = 0.01
POP_SIZE = 50
CROSSOVER = True
POLYGONS = 125
VERTICES = 4


def main():
    im = cv2.imread("../static/images/frog.jpeg",flags=cv2.IMREAD_COLOR)    

    population = Population(mutation_rate=MUTATION_RATE, pop_size=POP_SIZE, crossover=CROSSOVER, mutate=CROSSOVER, polygons=POLYGONS, vertices=VERTICES)
    population.setup(im)

    start = time.time() # measure elapsed time
    for i in range(NUM_GENERATIONS):
        population.new_generation(population.population_size, iteration=i)
        most_fit = population.get_most_fit_individual()
        file_name = "output/result" + "-popsize" + str(POP_SIZE) + "-gens" + str(NUM_GENERATIONS)
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




# # Runs the algorithm
# import numpy as np
# # from PIL import Image
# import cv2
# from population import Population 
# import time
# import numpy as np

# NUM_GENERATIONS = 20
# MUTATION_RATE = 0.01
# POP_SIZE = 75
# CROSSOVER = True
# POLYGONS = 200
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