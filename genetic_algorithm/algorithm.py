# Runs the algorithm
import numpy as np
from PIL import Image

def main():
    print("Hello World!")
    img = Image.open("static\images\starrynight.png")
    np_img = np.array(img)
    for i in range(90):
        np_img[i] = [255,0,0]
   

    pilImage = Image.fromarray(np_img)
    print(type(pilImage))
    pilImage.show()
    
if __name__ == "__main__":
    main()