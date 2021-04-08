# DataProcessing.py
# 03-04-2021
# This file is for processing some .txt file and convert them to the string type.
# Also, it includes all static functions that other scripts may need.
#
# https://github.com/Yebulabula/STD_FINAL_YEAR
#
# Author Ye Mao
# King's College London
# Version 1.0

import os.path


def delete(data, index):
    """
        The function to delete symbol at input index.
        :param data: (string) The input data for delete.
        :param index: (int) The index of deleted symbol
        :return: (string) The string data after deletion.
    """
    return data[:index] + data[index + 1:]


def readFile(filename):
    """
        The function to read the file and store the content the file as string type.
        :param filename: (string) The path and the filename of the file
        :return data: (string) The string type data
    """
    if not os.path.isfile(filename): return None
    with open(filename, 'r') as text_file:
        data = text_file.read()
    return data


def readMultiLineFile(filename):
    """
        The function to read the file that contains multi-lines and store the content the file as string type.
        :param filename: (string) The path and the filename of the file
        :return data: (string) The string type data
    """
    with open(filename) as f:
        content = f.readlines()  # read each line in the file.
    content = [x.strip() for x in content]
    return content
