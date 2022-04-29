import numpy as np
import random
import cv2


class Brushstroke():
    """Initialize the Brushstroke object, which will make up the Image object"""

    def __init__(self, target_dims):
        self.color = random.randrange(0, 255)
        self.brushNumber = 4
        self.brushes = self.load_brushes('brush_types')
        self.brush_type = random.randrange(0, self.brushNumber)

        # representation of the brush img in matrix form
        brush_rep = self.brushes[self.brush_type]

        self.posX = int(random.randrange(0, target_dims[0]))
        self.posY = int(random.randrange(0, target_dims[1]))
        # Figure out range of sizes of brushstrokes
        self.size = 0
        # Add rotation
        # Figure out what padding number should be?
        self.padding = 0
        # Gradient measures change in the image
        # Magnitude tells us how quickly the image is changing
        # Direction of the gradient tells us the direction in which the image is changing most rapidly.
        # TODO: Need to draw the whole image first to calculate gradient

    def load_brushes(self, path):
        brushes = []
        for i in range(self.brushNumber):
            brushes.append(cv2.imread(path + '/brush' + str(i) + '.png'))
        return brushes
