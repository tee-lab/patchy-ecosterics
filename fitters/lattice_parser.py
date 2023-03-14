from pickle import load


def load_lattices(path):
    with open(path, 'rb') as file:
        return load(file)