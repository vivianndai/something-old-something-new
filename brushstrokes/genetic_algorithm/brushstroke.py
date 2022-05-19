import numpy as np
import random
import cv2


class Brushstroke():
    """Initialize the Brushstroke object, which will make up the Image object"""

    def __init__(self, target_dims):
        self.blue = random.randrange(0, 255)
        self.green = random.randrange(0, 255)
        self.red = random.randrange(0, 255)
        self.brushNumber = 4
        self.brushes = self.load_brushes(
            "../brush_types")

        self.brush_type = random.randrange(0, self.brushNumber)

        # representation of the brush img in matrix form
        self.brush_matrix = self.brushes[self.brush_type]

        self.scale_percent = random.randrange(
            5, 20)  # percent of original size
        # self.scale_percent = np.random.uniform(start, stop)
        width = int(self.brush_matrix.shape[1] * self.scale_percent / 100)
        height = int(self.brush_matrix.shape[0] * self.scale_percent / 100)
        dim = (width, height)

        self.brush_rep = cv2.resize(
            self.brush_matrix, dim, interpolation=cv2.INTER_AREA)

        # makes the opaque part of an image a random color
        # (completely opaque images have the alpha channel set to 255, transparent images set to 0)
        self.brush_rep[np.all(self.brush_rep == (
            0, 0, 0, 255), axis=-1)] = (self.blue, self.green, self.red, 255)

        self.size = (self.brush_rep.shape[0], self.brush_rep.shape[1])

        random_posX = int(random.randrange(0, target_dims[1]) - width)
        random_posY = int(random.randrange(0, target_dims[0]) - height)

        self.posX = 0 if random_posX < 0 else random_posX
        self.posY = 0 if random_posY < 0 else random_posY

    def load_brushes(self, path):
        brushes = []
        for i in range(self.brushNumber):
            brushes.append(cv2.imread(
                (path + "/brush" + str(i) + ".png"), cv2.IMREAD_UNCHANGED))
            # brushes.append(cv2.imread(path + '/brush' + str(i) + '.png'))
        return brushes
