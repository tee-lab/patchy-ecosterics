from concurrent.futures import ThreadPoolExecutor
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random

import os

from cluster_dynamics import get_cluster_dynamics


@njit(nogil=True, fastmath=True)
def update(lattice, birth_probability):
    changed_coords = None
    i, j = get_random_site(lattice)

    if i == -1 and j == -1:
        # no active sites
        return lattice, changed_coords
    else:
        if random() < birth_probability:
            # birth
            new_i, new_j = get_random_neighbour(i, j)
            if lattice[new_i, new_j] == 0:
                changed_coords = (new_i, new_j)
            lattice[new_i, new_j] = 1
        else:
            # death
            lattice[i, j] = 0
            changed_coords = (i, j)

    return lattice, changed_coords


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


def simulate(data):
    simulation_index, save_series, save_cluster = data
    lattice = randint(0, 2, (length, length))

    series_data = [copy(lattice)]
    cluster_data = []

    if simulation_index == 0:
        print("Compiling functions...")

    for i in range(time):
        old_lattice = copy(lattice)
        new_lattice, changed_coords = update(lattice, birth_probability)

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
    info_string = f"Contact process with birth probability = {birth_probability}\n"

    data = {}
    if format_type == "series":
        data["series_data"] = array(automaton_data, dtype=bool)
    elif format_type == "cluster":
        data["cluster_data"] = automaton_data
    data["info"] = info_string
    dump(data, open(save_path, 'wb'))


def contact_spatial(p = 0.5, num_parallel = 10, save_series = False, save_cluster = False):
    # model parameters
    global length, time, birth_probability
    
    length = 100
    time = 100
    birth_probability = p

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
    print(contact_spatial(0.75, 1, save_series=True, save_cluster=True))