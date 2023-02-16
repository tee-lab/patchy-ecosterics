from concurrent.futures import ThreadPoolExecutor
from math import sqrt
from multiprocessing import Pool
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random

import os

from cluster_dynamics import get_cluster_dynamics


def landscape_update(lattice, f_carrying, r_influence, immediacy):
    """ Simulates N^2 Monte Carlo steps of the automaton """
    length = len(lattice)
    
    for _ in range(length * length):
        f_current = sum(lattice) / (length * length)
        i = int(random() * length)
        j = int(random() * length)
        rho = get_density(lattice, i, j, r_influence, immediacy)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
        else:
            prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0

    return lattice


def single_update(lattice, f_carrying, r_influence, immediacy):
    """ Simulates a single Monte Carlo step of the automaton """
    length = len(lattice)

    f_current = sum(lattice) / (length * length)
    changed_coords = None
    i = int(random() * length)
    j = int(random() * length)
    rho = get_density(lattice, i, j, r_influence, immediacy)

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


def get_density(lattice, i, j, r_influence, immediacy):
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
    simulation_index, save_series, save_cluster, length, eq_time, simulation_time, f_carrying, r_influence, immediacy = data
    lattice = randint(0, 2, (length, length))

    density_data = []
    series_data = []
    cluster_data = []

    for i in range(eq_time): 
        lattice = landscape_update(lattice, f_carrying, r_influence, immediacy)

        # save density and series data
        density_data.append(sum(lattice) / (length * length))
        if save_series:
            series_data.append(copy(lattice))

        # show progress
        if simulation_index == 0:
            print(f"Equilibriation: {round(i * 100 / eq_time)} %", end="\r")

    if simulation_index == 0:
        print("Equilibriation: 100 %\n", end="\r")

    for i in range(int(simulation_time * length * length)):
        # single update
        old_lattice = copy(lattice)
        new_lattice, changed_coords = single_update(lattice, f_carrying, r_influence, immediacy)

        # save cluster data
        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
                cluster_data.append(status)

        # periodic saving of series and density data
        if (i % (length * length)) == 0:
            density_data.append(sum(lattice) / (length * length))

            if save_series:
                series_data.append(copy(lattice))

        # show progress
        if simulation_index == 0:
            print(f"Simulation: {round(i * 100 / (simulation_time * length * length), 2)} %", end="\r")

    if simulation_index == 0:
        print("Simulation: 100.00 %\n", end="\r")

    if len(series_data) == 1:
        series_data = None
    if cluster_data == []:
        cluster_data = None
    if simulation_time == 0:
        new_lattice = copy(lattice)

    records = [density_data, cluster_data, series_data, new_lattice]
    return records


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702

    return max(slope * rainfall + intercept, 0)


def save_data(record, rainfall):
    """ Saves the entire simulation data in a pickle file, in the same folder """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(current_path)
    precursor_file_name = "simulation" + "_"

    num_files = 0
    for file_name in files_list:
        if file_name.startswith(precursor_file_name) and file_name.endswith(".pkl"):
            num_files += 1

    file_name = f"{precursor_file_name}{num_files}.pkl"
    save_path = os.path.join(current_path, file_name)
    info_string = f"Scanlon model with rainfall: {rainfall}\n"

    # save everything available
    data = {}
    density_data, cluster_data, series_data, final_lattice = record
    data["info"] = info_string
    data["density_data"] = density_data
    data["final_lattice"] = final_lattice
    
    if cluster_data is not None:
        data["cluster_data"] = cluster_data
    if series_data is not None:
        data["series_data"] = array(series_data, dtype=bool)
    
    dump(data, open(save_path, 'wb'))


def scanlon_kalahari(rainfall_ext = 800, num_parallel = 10, save_series = False, save_cluster = True):
    # model parameters
    global length, rainfall, f_carrying, r_influence, immediacy, eq_time, simulation_time
    length = 100
    rainfall = rainfall_ext
    f_carrying = get_forest_cover(rainfall)
    r_influence = 6
    immediacy = 10

    eq_time = 100
    simulation_time = 100

    print(f"Simulating {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster, length, eq_time, simulation_time, f_carrying, r_influence, immediacy) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        save_data(record, rainfall)

    avg_final_density = 0
    for record in records:
        _, _, _, final_lattice = record
        avg_final_density += sum(final_lattice) / (length * length)
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    scanlon_kalahari(600, 4, save_series=True, save_cluster=True)