from multiprocessing import Pool
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random
import os

from cluster_dynamics import get_cluster_dynamics


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


def single_update(lattice, p, q):
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
    simulation_index, save_series, save_cluster, length, eq_time, simulation_time, p, q = data
    lattice = randint(0, 2, (length, length))

    density_data = []
    series_data = []
    cluster_data = []

    for i in range(eq_time): 
        lattice = landscape_update(lattice, p, q)

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
        new_lattice, changed_coords = single_update(lattice, p, q)

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

    records = [density_data, cluster_data, series_data, new_lattice]
    return records


def save_data(record, p, q):
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
    info_string = f"TDP with p: {p}, q: {q}\n"

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


def tricritical(p_ext = 0.5, q_ext = 0.5, num_parallel = 10, save_series = False, save_cluster = True):
    # model parameters
    length = 100
    eq_time = 100
    simulation_time = 100
    p = p_ext
    q = q_ext

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster, length, eq_time, simulation_time, p, q) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        save_data(record, p, q)

    avg_final_density = 0
    for record in records:
        density_data, _, _, _ = record
        avg_final_density += density_data[-1]
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    print(tricritical(0.4, 0.92, 4, save_series=True, save_cluster=True))