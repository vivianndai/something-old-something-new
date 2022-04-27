# Runs the algorithm
import numpy as np
# from PIL import Image
import cv2
from population import Population 


def main():
    im = cv2.imread("../static/images/small.jpeg",flags=cv2.IMREAD_COLOR)    
    # cv2.imwrite('filename.jpeg', im)

    population = Population(mutation_rate=0.01, pop_size=20, crossover=True, mutate=True)
    # print(type(population.population[0]))
    population.setup(im)

    num_gens = 5
    for i in range(num_gens):
        population.new_generation(population.population_size, iteration=i)
    
    most_fit = population.get_most_fit_individual()
    file_name = "output/result" + "-popsize" + str(population.population_size) + "-gens" + str(num_gens)
    if population.crossover:
        file_name += "-crossover"
    if population.mutate:
        file_name += "-mutate" + "-mut_rate" + str(population.mutation_rate)[2:]
    file_name += ".jpeg"

    cv2.imwrite(file_name, most_fit)

if __name__ == "__main__":
    main()