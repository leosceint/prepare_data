#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
from encode_img import *


def clear_directory(dir_path: str):
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)
    else:
        print("Directory '%s' already exists" % dir_path)
        for filename in os.listdir(dir_path):
            file_path = os.path.join(dir_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e_rr:
                print("Failed to delete ", file_path, "Reason: ", e_rr)
                exit(-1)
        print("Directory '%s' was cleaned" % dir_path)


def sorted_path(path_list: list):
    name, ext_list = path_list[0].split(".")
    try:
        _ = int(name)
    except ValueError:
        print("Name of files in LIST is not a number")
        print("Please use other function to sort your file names")
        raise ValueError

    names_as_number_list = sorted([int(path_name.split(".")[0]) for path_name in path_list])
    return [str(name_as_number) + "." + ext_list for name_as_number in names_as_number_list]


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--src', default=os.path.join("..", "src_imgs"))
    argument_parser.add_argument('-o', '--dst', default=os.path.join("..", "src_imgs2"))
    args = argument_parser.parse_args()

    in_imgs_dir = args.src
    out_imgs_dir = args.dst

    imgs_list = []

    try:
        imgs_list = sorted_path(os.listdir(in_imgs_dir))
    except FileNotFoundError:
        print("!! Input directory not found !!")
        os.mkdir(in_imgs_dir)
        print("WE MADE IT -- %s. Please copy data there" % in_imgs_dir)
        exit(-1)

    clear_directory(out_imgs_dir)

    if len(imgs_list) > 0:
        for img_index, img_name in enumerate(imgs_list):
            img_array = EncodeIMG(os.path.join(in_imgs_dir, img_name), img_index).get_encode_img()
            path_to_save = os.path.join(out_imgs_dir, img_name)
            img_array.save(path_to_save)
            print("#%d image saved in %s" % (img_index+1, path_to_save))
