"""
This is for grouping output .txt and .png files with a common prefix into a same folder
Essentially, the folder contains all data associated with a single realisation
"""


from numpy import arange
from os import listdir, makedirs, path
from shutil import move


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")
    params = [0.498, 0.502, 0.504, 0.506, 0.508, 0.52]
    prefixes = [str(p).replace('.', 'p') for p in params]

    for prefix in prefixes:
        makedirs(path.join(output_path, prefix), exist_ok=True)

    for output_file in listdir(output_path):
        if path.isdir(path.join(output_path, output_file)):
            continue

        for prefix in prefixes:
            if output_file.startswith(prefix + "_"):
                source = path.join(output_path, output_file)
                dest = path.join(output_path, prefix, output_file)
                move(source, dest)
                break