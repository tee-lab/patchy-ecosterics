from concurrent.futures import ThreadPoolExecutor
from numba import njit
from numpy import array, copy, sum
from numpy.random import random, randint
from skimage.measure import label

import os


@njit(nogil=True, fastmath=True)
def update(lattice, p, q):
    for _ in range(length * length):
        focal_i = randint(0, length)
        focal_j = randint(0, length)

        if lattice[focal_i, focal_j]:
            neigh_i, neigh_j = get_random_neighbour(focal_i, focal_j)

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
                    third_i, third_j = get_pair_neighbour(focal_i, focal_j, neigh_i, neigh_j)
                    lattice[third_i, third_j] = 1
                elif random() < 1 - p:
                    # pair death with probability with probability (1 - p) (1 - q)
                    lattice[focal_i, focal_j] = 0


@njit(nogil=True, fastmath=True)
def get_random_site(lattice):
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


@njit(nogil=True, fastmath=True)
def get_random_neighbour(i, j):
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


@njit(nogil=True, fastmath=True)
def get_pair_neighbour(i1, j1, i2, j2):
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


def simulate(simulation_index):
    lattice = randint(0, 2, (length, length))
    time_series = [copy(lattice)]

    if simulation_index == 0:
        print("Compiling functions...")

    for i in range(time):
        update(lattice, p, q)
        time_series.append(copy(lattice))
        if simulation_index == 0:
            print(f"{i * 100 / time} %", end="\r")

    return time_series


def row_has_cluster(labelled_lattice, row, cluster):
    for j in range(length):
        if labelled_lattice[row, j] == cluster:
            return True
    return False


def col_has_cluster(labelled_lattice, col, cluster):
    for i in range(length):
        if labelled_lattice[i, col] == cluster:
            return True
    return False


def has_spanning_cluster(lattice):
    labelled_lattice = label(lattice, connectivity=1, background=0)
    num_labels = labelled_lattice.max()

    for i in range(1, num_labels + 1):
        if row_has_cluster(labelled_lattice, 0, i) and row_has_cluster(labelled_lattice, length - 1, i):
            if col_has_cluster(labelled_lattice, 0, i) and col_has_cluster(labelled_lattice, length - 1, i):
                return True

    return False


def tricritical(p_ext = 0.5, q_ext = 0.5, num_parallel = 10):
    # model parameters
    global length, time, p, q
    length = 100
    time = 500
    p = p_ext
    q = q_ext

    print(f"Simulating {num_parallel} automata in parallel...")
    with ThreadPoolExecutor(num_parallel) as pool:
        time_series_records = list(pool.map(simulate, range(num_parallel)))

    # calculate final density
    avg_final_density = 0
    for time_series in time_series_records:
        avg_final_density += sum(time_series[-1]) / (length * length)
    avg_final_density /= num_parallel

    # calculate percolation probability
    num_spanning_clusters = 0
    for time_series in time_series_records:
        if has_spanning_cluster(time_series[-1]):
            num_spanning_clusters += 1
    percolation_probability = num_spanning_clusters / num_parallel

    return avg_final_density, percolation_probability


if __name__ == '__main__':
    tricritical(0.36, 0.92, 10, True)