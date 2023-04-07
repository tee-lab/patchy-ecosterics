from math import floor, sqrt
from matplotlib import pyplot as plt
from multiprocessing import Pool
from numba import njit
from numpy import arange, array, copy, sum, zeros
from numpy.random import randint
from random import random
from skimage.measure import label
from tqdm import tqdm

import os


@njit(fastmath=True, nogil=True)
def landscape_update(lattice, f_carrying, r_influence, immediacy):
    """ Simulates a single Monte Carlo step of the automaton """
    length = len(lattice)
    f_current = sum(lattice) / (length * length)

    for _ in range(length * length):
        i = int(random() * length)
        j = int(random() * length)
        
        rho = get_density(lattice, r_influence, immediacy, i, j)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
                f_current += 1 / (length * length)
        else:
            prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0
                f_current -= 1 / (length * length)

    return lattice


@njit(fastmath=True, nogil=True)
def get_density(lattice, r_influence, immediacy, i, j):
    """ Calculates the vegetation density in the neighbourhood of a given cell (i, j) """
    length = len(lattice)
    normalization = 0
    density = 0

    for a in range(max(i - r_influence, 0), min(i + r_influence + 1, length)):
        for b in range(max(j - r_influence, 0), min(j + r_influence + 1, length)):
            distance = sqrt((a - i) ** 2 + (b - j) ** 2)
            if distance < r_influence:
                weightage_term = 1 - (distance / immediacy)
                density += weightage_term * lattice[a, b]
                normalization += weightage_term

    return density / normalization


def simulate(data):
    simulation_index, length, time, rainfall, r_influence, immediacy = data
    
    # initialize lattice and time series
    lattice = randint(0, 2, (length, length))
    f_carrying = get_forest_cover(rainfall)

    if simulation_index == 0:
        print("Simulating for rainfall = {}".format(rainfall))
        iterator = tqdm(range(time))
    else:
        iterator = range(time)

    # simulate
    for _ in iterator:
        lattice = landscape_update(lattice, f_carrying, r_influence, immediacy)

    density = sum(lattice) / (length * length)
    has_percolation = has_spanning_cluster(lattice)

    return density, has_percolation


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702

    return max(slope * rainfall + intercept, 0)


@njit
def row_has_cluster(labelled_lattice, row, cluster):
    length = len(labelled_lattice)
    for j in range(length):
        if labelled_lattice[row, j] == cluster:
            return True
    return False


@njit
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


def scanlon_kalahari(rainfall_ext, radius_ext, immediacy_ext, num_parallel = 10):
    # model parameters
    length = 500
    time = 200
    rainfall = rainfall_ext
    r_influence = radius_ext
    immediacy = immediacy_ext

    with Pool(num_parallel) as pool:
        data = pool.map(simulate, [(i, length, time, rainfall, r_influence, immediacy) for i in range(num_parallel)])

    avg_density = sum([d for d, _ in data]) / num_parallel
    percolation_probablity = sum([p for _, p in data]) / num_parallel

    return avg_density, percolation_probablity


if __name__ == '__main__':
    num_simulations = 10
    rainfall_values = arange(300, 1000, 100)
    percolation_probablities = zeros(len(rainfall_values), dtype=float)

    for i, rainfall in enumerate(rainfall_values):
        d, p = scanlon_kalahari(rainfall, num_simulations)
        
        print(d, p)
        percolation_probablities[i] = p

    plt.title(f"Percolation probability vs birth probability for Scanlon Kalahari model")
    plt.xlabel("Rainfall")
    plt.ylabel("Percolation probability")
    plt.plot(rainfall_values, percolation_probablities)
    plt.savefig("percolation_probability.png")
    plt.show()