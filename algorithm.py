import numpy as np
import random
import cv2


class BrushStroke():
    # Brushstroke is a member of the population (painting)

    def _init_(self, target_dims):
        self.color = random.randrange(0, 255)
        self.brushNumber = 4
        self.brushes = self.load_brushes('brush_types')
        self.brush_type = random.choice(self.brushes)

        self.posX = int(random.randrange(0, target_dims[0]))
        self.posY = int(random.randrange(0, target_dims[1]))
        # Figure out range of sizes of brushstrokes
        self.size = 0
        self.fitness = 0.0
        self.genes = np.array[self.color,
                              self.brush_type, self.posX, self.posY]
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
            brushes.append(cv2.imread(path + 'brush' + str(i) + '.png'))

    def mutate(self, brushstroke):
        rand = np.random.randint(4)
        if rand == 0:
            brushstroke.color = random.randrange(0, 255)
        elif rand == 1:
            brushstroke.brush_type = random.choice(self.brushes)
        elif rand == 2:
            brushstroke.posX = int(random.randrange(0, target_dims[0]))
        elif rand == 3:
            brushstroke.posY = int(random.randrange(0, target_dims[1]))

    def draw_brushstroke(self, brushstroke, target_img):
        color = brushstroke.genes[0]
        brush = brushstroke.genes[1]
        posX = brushstroke.genes[2] + self.padding
        posY = brushstroke.genes[3] + self.padding
        size = brushstroke.genes[4]

        # test which interpolation method is best
        brush_resized = cv2.resize(
            brush, None, fx=size, fy=size, interpolation=cv2.INTER_LINEAR)
        rows = brush_resized.shape(0)
        columns = brush_resized.shape(1)

        y_min = int(posY - rows/2)
        y_max = int(posY + (rows - rows/2))
        x_min = int(posX - columns/2)
        x_max = int(posX + (columns - columns/2))

        brush_img = np.copy(brush_resized)[0:rows, 0:columns].astype(float)
        canvas = target_img[y_min: y_max, x_min: x_max].astype(float)
        out = cv2.add(brush_img, canvas).astype(int)
        return out

    def draw_canvas(self, brushstroke_seq, target_img):
        img = 0
        for brushstroke in brushstroke_seq:
            self.draw_brushstroke(brushstroke, img)
