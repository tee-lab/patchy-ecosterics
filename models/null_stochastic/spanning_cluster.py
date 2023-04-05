from math import exp
from multiprocessing import Pool
from numba import njit
from numpy import array, copy, sum, zeros
from numpy.random import random, randint
from pickle import dump
from skimage.measure import label
from tqdm import tqdm
import os

from cluster_dynamics import get_cluster_dynamics, get_changed_lattice


@njit
def landscape_update(lattice, r, m):
    length = len(lattice)

    for _ in range(length * length):
        i = randint(0, length)
        j = randint(0, length)

        if lattice[i, j] == 0:
            if random() < r:
                lattice[i, j] = 1
        else:
            if random() < m:
                lattice[i, j] = 0

    return lattice


def get_init_lattice(length, req_occupancy):
    lattice = zeros((length, length))
    
    for i in range(length):
        for j in range(length):
            if random() < req_occupancy:
                lattice[i, j] = 1

    return lattice


def simulate(data):
    simulation_index, fractional_cover, length, time = data

    lattice = get_init_lattice(length, fractional_cover)

    if fractional_cover <= 0:
        m = 1
        r = 0
    elif fractional_cover >= 1:
        r = 1
        m = 0
    else:
        m = 1 - fractional_cover
        m_by_r = 1 / fractional_cover - 1
        r = 1 / (m_by_r / m)

    if simulation_index == 0:
        print(f"Simulation f = {fractional_cover:.3f}")
        iterator = tqdm(range(time))
    else:
        iterator = range(time)

    for _ in iterator:
        lattice = landscape_update(lattice, r, m)

    density = sum(lattice) / (length * length)
    has_percolation = has_spanning_cluster(lattice)

    return density, has_percolation


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


def null_stochastic(fractional_cover, num_parallel = 10):
    # model parameters
    length = 500
    time = 500

    data = [(simulation_index, fractional_cover, length, time) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        data = list(pool.map(simulate, data))

    avg_density = sum([datum[0] for datum in data]) / num_parallel
    percolation_probability = sum([datum[1] for datum in data]) / num_parallel

    return avg_density, percolation_probability


if __name__ == '__main__':
    null_stochastic(0.5, num_parallel=4, save_cluster=False)