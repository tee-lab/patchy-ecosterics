from math import exp
from multiprocessing import Pool
from numpy import array, copy, sum, zeros
from numpy.random import random, randint
from skimage.measure import label
import os


def single_update(lattice, r, m):
    changed_coords = None
    length = len(lattice)
    
    i = randint(0, length)
    j = randint(0, length)

    if lattice[i, j] == 0:
        if random() < r:
            lattice[i, j] = 1
            changed_coords = (i, j)
    else:
        if random() < m:
            lattice[i, j] = 0
            changed_coords = (i, j)

    return lattice, changed_coords


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
    time_series = [lattice]

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

    for i in range(time):
        lattice = landscape_update(lattice, r, m)
        time_series.append(copy(lattice))

        if simulation_index == 0:
            print(f"Equilibration: {round(i * 100 / time, 2)} %", end="\r")

    if simulation_index == 0:
        print("Equilibration: 100.00 %\n", end="\r")

    return time_series


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

    for i in range(1, num_labels + 1):
        if row_has_cluster(labelled_lattice, 0, i) and row_has_cluster(labelled_lattice, length - 1, i):
            if col_has_cluster(labelled_lattice, 0, i) and col_has_cluster(labelled_lattice, length - 1, i):
                return True

    return False


def null_stochastic(fractional_cover, num_parallel = 10):
    # model parameters
    length = 100
    time = 100

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, fractional_cover, length, time) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        time_series_records = list(pool.map(simulate, data))

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
    null_stochastic(1, num_parallel=4)