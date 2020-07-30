#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
import io


class NumberChannelsError(Exception):

    def __str__(self):
        return "Invalid number of channel! Must be 1, 3 or 4."


class EncodeIMG:

    def __init__(self, img_path: str, num: int, bins=32, width=640):
        self.img = np.array(Image.open(img_path))
        self.num = num
        self.bins = bins
        self.width = width

    def to_bin(self):
        values = list(int(b) for b in (np.binary_repr(self.num)))
        bits = np.zeros(self.bins, dtype='uint8')
        bits[-len(values):] = values
        times = int(self.width / self.bins)
        bits = np.repeat(bits, times)
        return bits

    def get_encode_img(self):
        row = self.to_bin()
        row *= 255

        if self.img.shape[-1] == 1:
            self.img[-1, :, :] = row

        elif self.img.shape[-1] == 3:
            self.img[-1, :, 0] = row
            self.img[-1, :, 1] = row
            self.img[-1, :, 2] = row

        elif self.img.shape[-1] == 4:
            self.img[-1, :, 0] = row
            self.img[-1, :, 1] = row
            self.img[-1, :, 2] = row
            self.img[-1, :, 3] = 255

        else:
            raise NumberChannelsError

        img_array = Image.fromarray(self.img)

        return img_array


if __name__ == '__main__':
    encode_img = EncodeIMG('10001.png', 12).get_encode_img()
