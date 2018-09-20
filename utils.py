# coding: utf-8
from PIL import Image
import numpy as np


def str_turn_num(c):
    if c in ['9', 'o', 'z']:
        print '存在错误数据'
    return (lambda x: x - 87 if x >= 97 else x - 48)(ord(c))


def num_turn_chr(c):
    if c < 10:
        k = chr(c + 48)
    else:
        k = chr(c + 87)
    return k


def denoise_img(img):
    '''图片降噪处理'''
    img2 = Image.new("L", img.size, 255)
    for x in range(img.size[1]):
        for y in range(img.size[0]):
            pix = img.getpixel((y, x))
            if pix == 17:  # these are the numbers to get
                img2.putpixel((y, x), 0)
    return img2


def get_img_data(img):
    x_size, y_size = img.size
    y_size -= 5
    piece = (x_size-22) / 8
    centers = [4+piece*(2*i+1) for i in range(4)]
    X = []
    for i, center in enumerate(centers):
        split_img = img.crop((center-(piece+2), 1, center+(piece+2), y_size))
        width, height = split_img.size
        X_a = []
        for h in range(0, height):
            for w in range(0, width):
                pixel = split_img.getpixel((w, h))
                if pixel == 255:
                    X_a.append(1)
                else:
                    X_a.append(0)
        X.append(X_a)
    return X


class LoadData():
    in_size = 336
    out_size = 36
    cursor = 0

    def __init__(self, file="data.dat"):
        data = np.loadtxt(file)
        print(len(data))
        y = data[:, self.in_size].reshape((-1, 1))
        self.g_y = np.rint(y == range(self.out_size))
        self.g_X = data[:, :self.in_size]

    def next_batch(self, batch):
        X_train = self.g_X[self.cursor:self.cursor+batch]
        y_train = self.g_y[self.cursor:self.cursor+batch]
        self.cursor += batch
        return X_train, y_train

    @property
    def test_xs(self):
        return self.g_X[-100:]

    @property
    def test_ys(self):
        return self.g_y[-100:]
