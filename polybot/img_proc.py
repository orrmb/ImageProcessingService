from pathlib import Path
from matplotlib.image import imread, imsave
import random


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray


class Img:

    def __init__(self, path):
        """
        Do not change the constructor implementation
        """
        self.path = Path(path)
        self.data = rgb2gray(imread(path)).tolist()

    def save_img(self):
        """
        Do not change the below implementation
        """
        new_path = self.path.with_name(self.path.stem + '_filtered' + self.path.suffix)
        imsave(new_path, self.data, cmap='gray')
        return new_path

    def blur(self, blur_level=16):

        height = len(self.data)
        width = len(self.data[0])
        filter_sum = blur_level ** 2

        result = []
        for i in range(height - blur_level + 1):
            row_result = []
            for j in range(width - blur_level + 1):
                sub_matrix = [row[j:j + blur_level] for row in self.data[i:i + blur_level]]
                average = sum(sum(sub_row) for sub_row in sub_matrix) // filter_sum
                row_result.append(average)
            result.append(row_result)

        self.data = result

    def contour(self):
        for i, row in enumerate(self.data):
            res = []
            for j in range(1, len(row)):
                res.append(abs(row[j-1] - row[j]))

            self.data[i] = res

    def rotate(self):
        width = len(self.data)
        high = len(self.data)
        m = 0


        row , cols = (width , high)
        arr = [[ 0 for i in range(row)] for j in range(cols)]

        for g in range(width):
            for k in range(high):
                arr[g][k] = self.data[g][k]


        for i in range(len(arr)):
            for j in arr[i]:
                for m in range(high -1, 0, -1 ):
                    self.data[i][m] = j
           

    def salt_n_pepper(self):
        for i in range(len(self.data)):
            for x in range(len(self.data[i])):
                rand_num = random.uniform(0, 1)
                if rand_num < 0.2:
                    self.data[i][x] = 255
                elif rand_num > 0.8:
                    self.data[i][x] = 0


    def concat(self, other_img, direction='horizontal'):
        height_other = len(other_img.data)
        width_other = len(other_img.data[0])
        height_self = len(self.data)
        width_self = len(self.data[0])
        try:
            if height_other == height_self and width_self == width_other:
                for i in range(height_other):
                    self.data[i] = self.data[i] + other_img.data[i]
        except:
            raise RuntimeError("Please Enter 2 pictures in the same Dimensions")

    def segment(self):
        for i in range(len(self.data)):
            for x in range(len(self.data[i])):
                if self.data[i][x] >= 100:
                    self.data[i][x] = 255
                else:
                    self.data[i][x] = 0



if __name__== '__main__':
    my_img = Img('test/beatles.jpeg')
    other_img = Img('test/beatles.jpeg')
    my_img.rotate()
    my_img.save_img()