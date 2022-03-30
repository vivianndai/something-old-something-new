# Runs the algorithm
import numpy as np
# from PIL import Image
import cv2
from population import Population 


def main():
    im = cv2.imread("../static/images/starrynight.png",flags=cv2.IMREAD_COLOR)
    for i in range(90):
        im[i] = [255,0,0]
    
    cv2.imwrite('filename.jpeg', im)

    population = Population(0.1, 5)
    print(type(population.population[0]))
    population.setup(im)

    for i in range(1):
        population.new_generation(population.population_size)
    
if __name__ == "__main__":
    main()