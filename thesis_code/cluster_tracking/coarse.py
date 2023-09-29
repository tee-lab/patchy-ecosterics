from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from multiprocessing import Pool, set_start_method
from numba import njit
from numpy import array, copy, sum, zeros
from numpy.random import random, randint
from pickle import dump
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


def tricritical(p = 0.5, q = 0.5, diff = 1):
    # model parameters
    length = 10
    eq_time = 1000
    
    lattice = randint(0, 2, (length, length))
    lattice = (lattice == 1).astype(int)

    for _ in range(eq_time):
        lattice = landscape_update(lattice, p, q)

    old_lattice = copy(lattice)
    for _ in range(diff):
        lattice = landscape_update(lattice, p, q)
    new_lattice = copy(lattice)

    difference_map = new_lattice - old_lattice
    
    plt.figure(figsize=(15, 5))
    plt.subplot(131)
    plt.title("Initial Lattice")
    plt.imshow(old_lattice)
    plt.subplot(132)
    plt.title("Lattice after 10N^2 updates")
    plt.imshow(new_lattice)
    plt.subplot(133)
    plt.title("Difference Map")
    plt.imshow(difference_map)
    plt.savefig("coarse.png", bbox_inches='tight')
    plt.show()
    


if __name__ == '__main__':
    print(tricritical(0.72, 0.0, 10))