from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from numba import njit
from numpy import array, copy, sum
from numpy.random import random, randint
from skimage.measure import label
from tqdm import tqdm

import os


@njit
def landscape_update(lattice, p, q):
    length = len(lattice)

    for _ in range(length * length):
        focal_i = randint(0, length)
        focal_j = randint(0, length)

        if lattice[focal_i, focal_j]:
            neigh_i, neigh_j = get_random_neighbour(focal_i, focal_j, length)

            if lattice[neigh_i, neigh_j] == 0:
                if random() < p:
                    # contact process birth with probability p
                    lattice[neigh_i, neigh_j] = 1
                else:
                    # contact process death with probability 1 - p
                    lattice[focal_i, focal_j] = 0
            else:
                if random() < q:
                    # positive feedback birth with probability q
                    third_i, third_j = get_pair_neighbour(focal_i, focal_j, neigh_i, neigh_j, length)
                    lattice[third_i, third_j] = 1
                elif random() < 1 - p:
                    # pair death with probability with probability (1 - p) (1 - q)
                    lattice[focal_i, focal_j] = 0

    return lattice


@njit
def get_random_site(lattice):
    length = len(lattice)
    num_active = sum(lattice)

    if num_active == 0:
        return -1, -1
    elif num_active == 1:
        for i in range(length):
            for j in range(length):
                if lattice[i, j] == 1:
                    return i, j
    else:
        while True:
            i = randint(0, length)
            j = randint(0, length)
            if lattice[i, j] == 1:
                return i, j


@njit
def get_random_neighbour(i, j, length):
    neighbour = randint(0, 4)
    # periodic boundary conditon
    if neighbour == 0:
        return (i + 1) % length, j
    elif neighbour == 1:
        return (i - 1 + length) % length, j
    elif neighbour == 2:
        return i, (j + 1) % length
    elif neighbour == 3:
        return i, (j - 1 + length) % length


@njit
def get_pair_neighbour(i1, j1, i2, j2, length):
    neighbour = randint(0, 6)

    # periodic boundary condition
    if i1 == i2:
        # same row
        j_left = min(j1, j2)
        j_right = max(j1, j2)
        
        if neighbour == 0:
            # above the left cell
            return (i1 - 1 + length) % length, j_left
        elif neighbour == 1:
            # above the right cell
            return (i1 - 1 + length) % length, j_right
        elif neighbour == 2:
            # right of the right cell
            return i1, (j_right + 1) % length
        elif neighbour == 3:
            # below the right cell
            return (i1 + 1) % length, j_right
        elif neighbour == 4:
            # below the left cell
            return (i1 + 1) % length, j_left
        elif neighbour == 5:
            # left of the left cell
            return i1, (j_left - 1 + length) % length
    else:
        # same column
        i_top = min(i1, i2)
        i_bottom = max(i1, i2)

        if neighbour == 0:
            # above the top cell
            return (i_top - 1 + length) % length, j1
        elif neighbour == 1:
            # right of the top cell
            return i_top, (j1 + 1) % length
        elif neighbour == 2:
            # right of the bottom cell
            return i_bottom, (j1 + 1) % length
        elif neighbour == 3:
            # below the bottom cell
            return (i_bottom + 1) % length, j1
        elif neighbour == 4:
            # left of the bottom cell
            return i_bottom, (j1 - 1 + length) % length
        elif neighbour == 5:
            # left of the top cell
            return i_top, (j1 - 1 + length) % length


def simulate(data):
    simulation_index, length, time, p, q = data
    lattice = randint(0, 2, (length, length))
    lattice = (lattice == 1).astype(int)

    if simulation_index == 0:
        print(f"Simulating ({p:.3f}, {q:.2f})")
        iterator = tqdm(range(time))
    else:
        iterator = range(time)

    for _ in iterator: 
        lattice = landscape_update(lattice, p, q)

    density = sum(lattice) / (length * length)
    percolation = has_spanning_cluster(lattice)

    return density, percolation


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


def tricritical(p_ext = 0.5, q_ext = 0.5, num_parallel = 10):
    # model parameters
    global length, time, p, q
    length = 250
    time = 1000
    p = p_ext
    q = q_ext

    with Pool(num_parallel) as pool:
        data = pool.map(simulate, [(i, length, time, p, q) for i in range(num_parallel)])

    avg_final_density = sum([d[0] for d in data]) / num_parallel
    percolation_probability = sum([d[1] for d in data]) / num_parallel

    return avg_final_density, percolation_probability


if __name__ == '__main__':
    tricritical(0.36, 0.92, 10, True)