import numpy as np
import random
import cv2


class Brushstroke():
    """Initialize the Brushstroke object, which will make up the Image object"""

    def __init__(self, target_dims):
        self.color = random.randrange(0, 255)
        self.brushNumber = 4
        self.brushes = self.load_brushes(
            '/Users/connietsang/Desktop/ai/brushstrokes/brush_types')
        self.brush_type = random.randrange(0, self.brushNumber)

        # representation of the brush img in matrix form
        self.brush_matrix = self.brushes[self.brush_type]

        scale_percent = 30  # percent of original size
        width = int(self.brush_matrix.shape[1] * scale_percent / 100)
        height = int(self.brush_matrix.shape[0] * scale_percent / 100)
        dim = (width, height)

        self.brush_rep = cv2.resize(
            self.brush_matrix, dim, interpolation=cv2.INTER_AREA)

        # self.mask = self.brush_rep[:, :, 3]

        self.size = (self.brush_rep.shape[0], self.brush_rep.shape[1])

        self.posX = int(random.randrange(0, target_dims[0]) - width)
        self.posY = int(random.randrange(0, target_dims[1]) - height)

        # Gradient measures change in the image
        # Magnitude tells us how quickly the image is changing
        # Direction of the gradient tells us the direction in which the image is changing most rapidly.

    def load_brushes(self, path):
        brushes = []
        for i in range(self.brushNumber):
            brushes.append(cv2.imread(
                (path + '/brush' + str(i) + '.png'), cv2.IMREAD_UNCHANGED))
            # brushes.append(cv2.imread(path + '/brush' + str(i) + '.png'))
        return brushes
