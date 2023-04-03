from itertools import product
from matplotlib import pyplot as plt
from multiprocessing import Pool
from numpy import array, sum, zeros
from numpy.random import random
from skimage.measure import label


def generate_automaton(data):
    length, required_occupancy = data

    prob = random((length, length))
    lattice = (prob < required_occupancy).astype(int)

    density = sum(lattice) / (length * length)
    has_percolation = has_spanning_cluster(lattice)

    return density, has_percolation


def row_has_cluster(labelled_lattice, row, cluster):
    length = len(labelled_lattice)
    for j in range(length):
        if labelled_lattice[row, j] == cluster:
            return True
    return False


def col_has_cluster(labelled_lattice, col, cluster):
    length = len(labelled_lattice)
    for i in range(length):
        if labelled_lattice[i, col] == cluster:
            return True
    return False


def has_spanning_cluster(lattice):
    length = len(lattice)
    labelled_lattice = label(lattice, connectivity=1, background=0)
    num_labels = labelled_lattice.max()

    if num_labels == 0:
        return False
    
    sizes = [sum(labelled_lattice == i) for i in range(1, num_labels + 1)]
    biggest_cluster = sizes.index(max(sizes)) + 1

    if row_has_cluster(labelled_lattice, 0, biggest_cluster) and row_has_cluster(labelled_lattice, length - 1, biggest_cluster):
        return True
    elif col_has_cluster(labelled_lattice, 0, biggest_cluster) and col_has_cluster(labelled_lattice, length - 1, biggest_cluster):
        return True
    else:
        return False


def null_static(occupancy, num_parallel=10):
    length = 250

    with Pool(num_parallel) as pool:
        data = pool.map(generate_automaton, [(length, occupancy) for _ in range(num_parallel)])

    avg_density = sum([d[0] for d in data]) / len(data)
    percolation_probability = sum([d[1] for d in data]) / len(data)

    return avg_density, percolation_probability


if __name__ == '__main__':
    null_static(0.8)