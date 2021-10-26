import os
import shutil


def clear_directory(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)


def to_number(formatted_int):
    if formatted_int.endswith('k'):
        formatted_int = float(formatted_int.replace('k', ''))*1000
    return int(formatted_int)
