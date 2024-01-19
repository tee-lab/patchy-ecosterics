"""
This is for grouping output .txt and .png files with a common prefix into a same folder
Essentially, the folder contains all data associated with a single realisation
"""


from numpy import arange
from os import listdir, makedirs, path
from shutil import move


if __name__ == '__main__':
    output_path = path.join(path.dirname(__file__), "outputs")

    p_values = [0.54, 0.57]
    # p_values = [0.616, 0.618, 0.62, 0.625, 0.63, 0.64, 0.65, 0.7, 0.72]
    # p_values = [0.566, 0.569, 0.57, 0.575, 0.58, 0.59, 0.62, 0.64]
    # p_values = [0.498, 0.5, 0.502, 0.504, 0.506, 0.508, 0.51, 0.52, 0.53, 0.55]
    # p_values = [0.399, 0.4, 0.401, 0.403, 0.405, 0.41, 0.42]
    # p_values = [300, 400, 500, 600, 700, 770, 800, 830, 900]

    params = p_values
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