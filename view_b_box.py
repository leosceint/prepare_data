#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
from PIL import Image
import matplotlib.patches as patches
from matplotlib import pyplot as plt


# Предполагается, что в файле одна строчка с координатами
def read_coords(file_name: str):
    with open(file_name, "r") as file_with_coord:
        coord_data = file_with_coord.readlines()
    coords_list = []
    for line in coord_data:
        _, x_point, y_point, roi_width, roi_height = line.split(" ")
        coords_list.append((float(x_point), float(y_point), float(roi_width), float(roi_height)))
    return coords_list


if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--images', default=os.path.join("..", "src_imgs"))
    argument_parser.add_argument('-m', '--markups', default=os.path.join("..", "txt_markup"))
    argument_parser.add_argument('-n', '--number', default="1")
    args = argument_parser.parse_args()

    imgs_list = os.listdir(args.images)
    markup_list = os.listdir(args.markups)

    coord_list = read_coords(os.path.join(args.markups, markup_list[int(args.number)]))

    img = Image.open(os.path.join(args.images, imgs_list[int(args.number)]))
    img_width, img_height = img.size

    fig, ax = plt.subplots()
    img_plot = ax.imshow(img)

    for coord in coord_list:
        x1, y1, roi1_w, roi1_h = coord
        print("-== STAGE - 1 ==-")
        print("READ -- ", x1, y1, roi1_w, roi1_h)

        x1 = x1 * img_width
        y1 = y1 * img_height
        roi1_w = roi1_w * img_width
        roi1_h = roi1_h * img_height
        print("-== STAGE - 2 ==-")
        print("ABSOLUTE -- ", x1, y1, roi1_w, roi1_h)

        x1_left = x1 - 0.5 * roi1_w
        y1_left = y1 - 0.5 * roi1_h
        print("-== STAGE - 3 ==-")
        print("LEFT CORNER -- ", x1_left, y1_left, roi1_w, roi1_h)

        plt.scatter(x1, y1, s=3, facecolor='red')
        rect_calc = patches.Rectangle((x1_left, y1_left), roi1_w, roi1_h,
                                      linewidth=2, edgecolor="g", facecolor="none")
        ax.add_patch(rect_calc)

    plt.show()
