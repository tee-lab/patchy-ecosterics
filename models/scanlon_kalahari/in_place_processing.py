from concurrent.futures import ThreadPoolExecutor
from math import floor, sqrt
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random

import os

from cluster_dynamics import get_cluster_dynamics


@njit(fastmath=True, nogil=False)
def update(lattice):
    """ Simulates a single Monte Carlo step of the automaton """
    f_current = sum(lattice) / (length * length)
    changed_coords = None
    i = int(random() * length)
    j = int(random() * length)
    rho = get_density(lattice, i, j)

    if lattice[i, j] == 0:
        prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
        if random() < prob_growth:
            lattice[i, j] = 1
            changed_coords = (i, j)
    else:
        prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
        if random() < prob_decay:
            lattice[i, j] = 0
            changed_coords = (i, j)

    return lattice, changed_coords


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


def simulate(data):
    simulation_index, save_series, save_cluster = data
    lattice = randint(0, 2, (length, length))

    series_data = [copy(lattice)]
    cluster_data = []

    if simulation_index == 0:
        print("Compiling functions...")

    for i in range(time):
        old_lattice = copy(lattice)
        new_lattice, changed_coords = update(lattice)

        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
                cluster_data.append(status)

        if save_series:
            series_data.append(copy(new_lattice))

        if simulation_index == 0:
            print(f"{i * 100 / time} %", end="\r")

    if len(series_data) == 1:
        series_data = None
    if cluster_data == []:
        cluster_data = None

    records = [new_lattice, series_data, cluster_data]
    return records


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702

    return max(slope * rainfall + intercept, 0)


def save_data(automaton_data, format_type):
    """ Saves the entire simulation data in a pickle file, in the same folder """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(current_path)
    precursor_file_name = format_type + "_"

    num_files = 0
    for file_name in files_list:
        if file_name.startswith(precursor_file_name) and file_name.endswith(".pkl"):
            num_files += 1

    file_name = f"{precursor_file_name}{num_files}.pkl"
    save_path = os.path.join(current_path, file_name)
    info_string = f"Scanlon with rainfall = {rainfall} mm\n"

    data = {}
    if format_type == "series":
        data["series_data"] = array(automaton_data, dtype=bool)
    elif format_type == "cluster":
        data["cluster_data"] = automaton_data
    data["info"] = info_string
    dump(data, open(save_path, 'wb'))


def scanlon_kalahari(rainfall_ext = 800, num_parallel = 10, save_series = False, save_cluster = True):
    # model parameters
    global length, rainfall, f_carrying, r_influence, immediacy, time
    length = 100
    rainfall = rainfall_ext
    f_carrying = get_forest_cover(rainfall)
    r_influence = 9
    immediacy = 24
    time = 200

    print(f"Simulating {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster) for simulation_index in range(num_parallel)]
    with ThreadPoolExecutor(7) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        _, series_data, cluster_data = record
        if save_series:
            save_data(series_data, "series")
        if save_cluster:
            save_data(cluster_data, "cluster")

    avg_final_density = 0
    for record in records:
        final_lattice, _, _ = record
        avg_final_density += sum(final_lattice) / (length * length)
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    scanlon_kalahari(700, 1, save_series=True, save_cluster=True)