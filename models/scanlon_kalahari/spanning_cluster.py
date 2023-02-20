from concurrent.futures import ThreadPoolExecutor
from math import floor, sqrt
from matplotlib import pyplot as plt
from numba import njit
from numpy import arange, array, copy, sum, zeros
from numpy.random import randint
from pickle import dump
from random import random
from skimage.measure import label

import os


@njit(fastmath=True, nogil=False)
def mc_step(lattice):
    """ Simulates a single Monte Carlo step of the automaton """
    f_current = sum(lattice) / (length * length)

    for _ in range(mc_updates):
        i = int(random() * length)
        j = int(random() * length)
        rho = get_density(lattice, i, j)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
        else:
            prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0


@njit(fastmath=True, nogil=False)
def get_density(lattice, i, j):
    """ Calculates the vegetation density in the neighbourhood of a given cell (i, j) """
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


def simulate(simulation_index):
    print(f_carrying)
    
    # initialize lattice and time series
    lattice = randint(0, 2, (length, length))
    time_series = [copy(lattice)]

    if simulation_index == 0:
        print("Compiling functions...")

    # simulate
    for i in range(mc_steps):
        mc_step(lattice)
        time_series.append(copy(lattice))

        if simulation_index == 0:
            print(f"{i * 100 / mc_steps} %", end="\r")

    return time_series


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702

    return max(slope * rainfall + intercept, 0)


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


def scanlon_kalahari(rainfall_ext = 800, num_parallel = 10):
    # model parameters
    global length, rainfall, f_carrying, r_influence, immediacy
    length = 250
    rainfall = rainfall_ext
    f_carrying = get_forest_cover(rainfall)
    r_influence = 9
    immediacy = 24

    # simulation parameters
    global mc_steps, mc_updates
    mc_steps = 50
    mc_updates = floor(length * length)

    print(f"Simulating {num_parallel} automatons in parallel ...")
    with ThreadPoolExecutor(num_parallel) as pool:
        time_series_records = list(pool.map(simulate, range(num_parallel)))

    avg_final_density = 0
    for time_series in time_series_records:
        avg_final_density += sum(time_series[-1]) / (length * length)
    avg_final_density /= num_parallel

    num_spanning_clusters = 0
    for time_series in time_series_records:
        if has_spanning_cluster(time_series[-1]):
            num_spanning_clusters += 1
    percolation_probability = num_spanning_clusters / num_parallel

    return avg_final_density, percolation_probability


if __name__ == '__main__':
    num_simulations = 10
    rainfall_values = arange(300, 1000, 100)
    percolation_probablities = zeros(len(rainfall_values), dtype=float)

    for i, rainfall in enumerate(rainfall_values):
        print(f"\n---> Simulating rainfall = {rainfall} <---")
        d, p = scanlon_kalahari(rainfall, num_simulations)
        
        print(d, p)
        percolation_probablities[i] = p

    plt.title(f"Percolation probability vs birth probability for Scanlon Kalahari model")
    plt.xlabel("Rainfall")
    plt.ylabel("Percolation probability")
    plt.plot(rainfall_values, percolation_probablities)
    plt.savefig("percolation_probability.png")
    plt.show()