#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import shutil
import json


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


def translate_markup(json_name: str, jsons_dir: str, img_size: list):
    name_wo_ext, _ = json_name.split(".")
    img_width, img_height = img_size

    mark_lines = []

    with open(os.path.join(jsons_dir, json_name)) as json_file:
        json_data = json.load(json_file)
        i = 0
        for items_list in json_data:
            objectClass = items_list["objectClass"]
            if objectClass:
                i += 1
            region = items_list["region"]
            origin_point = region["origin"]
            abs_region_x = int(origin_point["x"])
            abs_region_y = int(origin_point["y"])
            size_point = region["size"]
            abs_region_width = int(size_point["width"])
            abs_region_height = int(size_point["height"])

            if args.mode == "raw":
                region_x = "{:.6f}".format(abs_region_x / img_width)
                region_y = "{:.6f}".format(abs_region_y / img_height)
            elif args.mode == "offset":
                region_x = "{:.6f}".format((abs_region_x + 0.5 * abs_region_width) / img_width)
                region_y = "{:.6f}".format((abs_region_y + 0.5 * abs_region_height) / img_height)

            region_width = "{:.6f}".format(abs_region_width / img_width)
            region_height = "{:.6f}".format(abs_region_height / img_height)
            print(objectClass, " : ", region_x, "; ", region_y, "|", region_width, "; ", region_height)
            mark_lines.append("%s %s %s %s %s\n" % (objectClass, region_x, region_y, region_width, region_height))

    print("%s file. Interested objects count - %s" % (json_name, str(i)))
    print("IMG size is %s x %s" % (img_width, img_height))

    return mark_lines


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-j', '--json_dir', default=os.path.join("..", "json_translate"))
    argument_parser.add_argument('-t', '--txt_dir', default=os.path.join("..", "txt_markup2"))
    argument_parser.add_argument('-s', '--size', default='640x480')
    argument_parser.add_argument('-m', '--mode', default='raw')
    args = argument_parser.parse_args()

    in_markup_dir = args.json_dir
    out_markup_dir = args.txt_dir
    imgs_size = [size for size in map(int, args.size.split('x'))]
    markup_list = []

    try:
        markup_list = sorted_path(os.listdir(in_markup_dir))
    except FileNotFoundError:
        print("!! Input directory not found !!")
        os.mkdir(in_markup_dir)
        print("WE MADE IT -- %s. Please copy data there" % in_markup_dir)
        exit(-1)

    clear_directory(out_markup_dir)

    if len(markup_list) > 0:
        for markup_index, markup_name in enumerate(markup_list):
            markup_lines = translate_markup(markup_name, in_markup_dir, imgs_size)

            path_to_save = os.path.join(out_markup_dir, markup_name.split(".")[0] + ".txt")

            with open(path_to_save, "w") as out_markup_file:
                out_markup_file.write("%s\n" % markup_index)
                out_markup_file.writelines(markup_lines)
            print("#%d image saved in %s" % (markup_index + 1, path_to_save))
