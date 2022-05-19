import numpy as np
import cv2
from brushstroke import Brushstroke


class Canvas():
    def __init__(self, target, p1=None, p2=None, crossover=False, mutate=False, mutation_rate=0.01, canvas=None):
        self.min_gene = 0
        self.max_gene = 255  # set these values for B/W, RGBA, etc
        self.gene_dims = np.shape(target)
        self.gene_len = self.gene_dims[0] * self.gene_dims[1]
        self.genes = np.zeros(self.gene_dims)
        self.target_dims = (target.shape[0], target.shape[1])
        self.fitness = 0
        self.brushstroke_list = []
        self.canvas = np.zeros(
            (self.target_dims[0], self.target_dims[1], 4), np.uint8)

    def combine_two_images_with_anchor(self, foreground, background, anchor_y, anchor_x):

        # Check if the foreground is inbound with coordinates

        foreground_height = foreground.shape[0]
        foreground_width = foreground.shape[1]
        background_height = background.shape[0]
        background_width = background.shape[1]
        if foreground_height+anchor_y > background_height or foreground_width+anchor_x > background_width:
            raise ValueError(
                "Target image is too small")

        alpha = 1

        # add foreground image to a portion of the background, then change
        # the rows and columns of the background to that blended portion
        start_y = anchor_y
        start_x = anchor_x
        end_y = anchor_y+foreground_height
        end_x = anchor_x+foreground_width

        blended_portion = cv2.addWeighted(foreground,
                                          alpha,
                                          background[start_y:end_y,
                                                     start_x:end_x, :],
                                          1 - alpha,
                                          0,
                                          background)

        for i in range(0, blended_portion.shape[0]):
            for j in range(0, blended_portion.shape[1]):
                v = blended_portion[i, j] == [255, 255, 255, 0]
                if v.any():
                    blended_portion[i, j] = background[i+anchor_y, j+anchor_x]

        background[start_y:end_y, start_x:end_x, :] = blended_portion

        # cv2.imshow('combined image', background)
        # cv2.imwrite(
        #     '/Users/connietsang/Desktop/ai/brushstrokes/combined_image.png', background)
        # cv2.waitKey(0)
        return background

    def draw_brushstroke(self, brushstroke, inImg):
        # inImg is initially empty
        brush = brushstroke.brush_rep
        posX = brushstroke.posX
        posY = brushstroke.posY
        out = self.combine_two_images_with_anchor(
            brush, inImg, posY, posX)
        return out

    def draw_canvas(self, brushstroke_seq):
        out = np.copy(self.canvas)
        for i in brushstroke_seq:
            out = self.draw_brushstroke(i, out)
        # cv2.imshow('canvas', out)
        # cv2.imwrite(
        #     '/Users/connietsang/Desktop/ai/brushstrokes/testcanvas.png', out)
        # cv2.waitKey(0)

        return out

    def calculate_fitness(self, brushstroke_seq, target_img):
        img = self.draw_canvas(brushstroke_seq)
        # error = cv2.norm(img, target_img)
        diff1 = cv2.subtract(img, target_img)
        diff2 = cv2.subtract(target_img, img)
        totalDiff = cv2.add(diff1, diff2)
        totalDiff = np.sum(totalDiff)
        self.fitness = totalDiff
        # self.fitness = 1-error/(target_img.shape[0] * target_img.shape[1])

    # returns a canvas with randomly generated brushstrokes
    def generate_random_canvas(self):
        for i in range(100):
            self.brushstroke_list.append(Brushstroke(
                [self.target_dims[0], self.target_dims[1]]))
        return self.draw_canvas(self.brushstroke_list)
