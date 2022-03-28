# Runs the algorithm
import numpy as np
from PIL import Image
from population import Population 


def main():
    print("Hello World!")
    img = Image.open("static\images\starrynight.png")
    np_img = np.array(img)
    for i in range(90):
        np_img[i] = [255,0,0]
   

    pilImage = Image.fromarray(np_img)
    print(type(pilImage))
    pilImage.show()

    population = Population(0.1, 100)
    population.setup(np_img)
    for i in range(100):
        population.new_generation(population.population_size)
        population.calculate_all_fitness()
    
if __name__ == "__main__":
    main()