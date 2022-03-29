# Runs the algorithm
import numpy as np
# from PIL import Image
import cv2
from population import Population 


def main():
    print("Hello World!")
    im = cv2.imread("starrynight.png",flags=cv2.IMREAD_COLOR)
    print(type(im))
    # img = Image.open("static\images\starrynight.png")
    # np_img = np.array(img)
    for i in range(90):
        im[i] = [255,0,0]
    

    cv2.imwrite('filename.jpeg', im)
    # pilImage = Image.fromarray(np_img)
    # print(type(pilImage))
    # pilImage.show()

    population = Population(0.1, 100)
    population.setup(im)
    for i in range(100):
        population.new_generation(population.population_size)
    
if __name__ == "__main__":
    main()