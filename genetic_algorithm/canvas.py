import numpy as np
import random
import cv2
from brushstroke import Brushstroke


class Canvas():
    def __init__(self, target, p1=None, p2=None, crossover=False, mutate=False, mutation_rate=0.01):
        self.min_gene = 0
        self.max_gene = 255  # set these values for B/W, RGBA, etc
        self.gene_dims = np.shape(target)
        self.gene_len = self.gene_dims[0] * self.gene_dims[1]
        self.genes = np.zeros(self.gene_dims)
        self.fitness = 0
        self.padding = 0
        # if crossover:
        #     self.crossover(p1, p2)
        # if mutate:
        #     self.mutate(rate=mutation_rate)
        # else:
        #     # choose a random matrix of genes (random pixel values for all genes)
        #     self.genes = np.random.randint(
        #         low=self.min_gene, high=self.max_gene, size=self.gene_dims)

        # self.calculate_fitness(target)

    def draw_brushstroke(self, brushstroke, target_img):
        color = brushstroke.color
        brush = brushstroke.brush_rep
        posX = brushstroke.posX + self.padding
        posY = brushstroke.posY + self.padding
        size = brushstroke.size

        # test which interpolation method is best/most efficient
        # could also just downsize
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
        out = [
            np.zeros((target_img.shape[0], target_img.shape[1]), np.uint8)]
        for i in range(len(brushstroke_seq)):
            temp_canvas = self.draw_brushstroke(brushstroke_seq[i], out)
            out = self.draw_brushstroke(brushstroke_seq[i+1], temp_canvas)
        return out

    def calculate_fitness(self, brushstroke_seq, target_img):
        img = self.draw_canvas(brushstroke_seq, target_img)
        error = cv2.norm(img, target_img)
        self.fitness = 1-error/(target_img.shape[0] * target_img.shape[1])
