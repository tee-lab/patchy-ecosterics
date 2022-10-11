from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random
import os

from cluster_dynamics import get_cluster_dynamics


def update(lattice, p, q):
    changed_coords = None
    length = len(lattice)
    focal_i = randint(0, length)
    focal_j = randint(0, length)

    if lattice[focal_i, focal_j]:
        neigh_i, neigh_j = get_random_neighbour(focal_i, focal_j, length)

        if lattice[neigh_i, neigh_j] == 0:
            if random() < p:
                # contact process birth with probability p
                lattice[neigh_i, neigh_j] = 1
                changed_coords = (neigh_i, neigh_j)
            else:
                # contact process death with probability 1 - p
                lattice[focal_i, focal_j] = 0
                changed_coords = (focal_i, focal_j)
        else:
            if random() < q:
                # positive feedback birth with probability q
                third_i, third_j = get_pair_neighbour(focal_i, focal_j, neigh_i, neigh_j, length)
                if lattice[third_i, third_j] == 0:
                    changed_coords = (third_i, third_j)
                lattice[third_i, third_j] = 1
            elif random() < 1 - p:
                # pair death with probability with probability (1 - p) (1 - q)
                lattice[focal_i, focal_j] = 0
                changed_coords = (focal_i, focal_j)

    return lattice, changed_coords


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


def get_pair_neighbour(i1, j1, i2, j2, length):
    neighbour = randint(0, 6)

    # periodic boundary condition
    if i1 == i2:
        # same row
        if neighbour == 0:
            return (i1 - 1 + length) % length, j1
        elif neighbour == 1:
            return (i1 - 1 + length) % length, j2
        elif neighbour == 2:
            return i1, (j2 + 1) % length
        elif neighbour == 3:
            return (i1 + 1) % length, j2
        elif neighbour == 4:
            return (i1 + 1) % length, j1
        elif neighbour == 5:
            return i1, (j1 - 1 + length) % length
    else:
        # same column
        if neighbour == 0:
            return (i1 - 1 + length) % length, j1
        elif neighbour == 1:
            return i1, (j1 + 1) % length
        elif neighbour == 2:
            return i2, (j1 + 1) % length
        elif neighbour == 3:
            return (i2 + 1) % length, j1
        elif neighbour == 4:
            return i2, (j1 - 1 + length) % length
        elif neighbour == 5:
            return i1, (j1 - 1 + length) % length


def simulate(data):
    simulation_index, save_series, save_cluster, length, time, p, q = data
    lattice = randint(0, 2, (length, length))

    series_data = [copy(lattice)]
    cluster_data = []

    if simulation_index == 0:
        print("Compiling functions...")

    for i in range(time):
        old_lattice = copy(lattice)
        new_lattice, changed_coords = update(lattice, p, q)

        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
                cluster_data.append(status)

        if save_series and (i % (length * length)) == 0:
            series_data.append(copy(new_lattice))

        if simulation_index == 0:
            print(f"{i * 100 / time} %", end="\r")

    if len(series_data) == 1:
        series_data = None
    if cluster_data == []:
        cluster_data = None

    records = [new_lattice, series_data, cluster_data]
    return records


def save_data(automaton_data, format_type, p, q):
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
    info_string = f"TDP with p: {p}, q: {q}\n"

    data = {}
    if format_type == "series":
        data["series_data"] = array(automaton_data, dtype=bool)
    elif format_type == "cluster":
        data["cluster_data"] = automaton_data
    data["info"] = info_string
    dump(data, open(save_path, 'wb'))


def tricritical(p_ext = 0.5, q_ext = 0.5, num_parallel = 10, save_series = False, save_cluster = True):
    # model parameters
    length = 100
    time = 500 * length * length
    p = p_ext
    q = q_ext

    print(f"Simulating {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster, length, time, p, q) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        _, series_data, cluster_data = record
        if save_series:
            save_data(series_data, "series", p, q)
        if save_cluster:
            save_data(cluster_data, "cluster", p, q)

    avg_final_density = 0
    for record in records:
        final_lattice, _, _ = record
        avg_final_density += sum(final_lattice) / (length * length)
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    print(tricritical(0.4, 0.92, 6, save_series=False, save_cluster=True))