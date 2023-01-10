from math import exp
from multiprocessing import Pool
from numpy import array, copy, sum
from numpy.random import random, randint
from pickle import dump
import os

from cluster_dynamics import get_cluster_dynamics


def single_update(lattice, req_occupancy):
    changed_coords = None
    length = len(lattice)
    init_occupancy = sum(lattice) / (length * length)
    init_diff = abs(init_occupancy - req_occupancy)

    # flip a random cell
    i = randint(0, length)
    j = randint(0, length)
    if lattice[i, j] == 0:
        lattice[i, j] = 1
    else:
        lattice[i, j] = 0

    final_occupancy = sum(lattice) / (length * length)
    final_diff = abs(final_occupancy - req_occupancy)

    if final_diff < init_diff:
        # readily accept flips that make the system go towards the required occupancy
        changed_coords = (i, j)
    else:
        # if the flip makes the system go away from the required occupancy
        # then the occurrence of that flip is penalized according to the difference of the system from the required occupancy
        energy = abs(final_occupancy - req_occupancy)
        acceptance_probability = exp(-energy)
        if random() < acceptance_probability:
            # accept the flip
            changed_coords = (i, j)
        else:
            # reverse the flip
            if lattice[i, j] == 0:
                lattice[i, j] = 1
            else:
                lattice[i, j] = 0

    return lattice, changed_coords


def simulate(data):
    simulation_index, save_cluster, init_lattice, time = data

    lattice = init_lattice
    length = len(init_lattice)
    req_occupancy = sum(init_lattice) / (length * length)

    density_data = []
    cluster_data = []

    for i in range(int(time * length * length)):
        # single update
        old_lattice = copy(lattice)
        new_lattice, changed_coords = single_update(lattice, req_occupancy)

        # save cluster data
        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                status = get_cluster_dynamics(old_lattice, new_lattice, changed_coords)
                cluster_data.append(status)

        # periodic saving of density data
        if (i % (length * length)) == 0:
            density_data.append(sum(lattice) / (length * length))

        # show progress
        if simulation_index == 0:
            print(f"Simulation: {round(i * 100 / (time * length * length), 2)} %", end="\r")

    if simulation_index == 0:
        print("Simulation: 100.00 %\n", end="\r")

    records = [density_data, cluster_data, new_lattice]
    return records


def save_data(record):
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
    info_string = f"Null Ising model\n"

    # save everything available
    data = {}
    density_data, cluster_data, final_lattice = record
    data["info"] = info_string
    data["density_data"] = density_data
    data["final_lattice"] = final_lattice
    data["series_data"] = None
    data["cluster_data"] = cluster_data
    
    dump(data, open(save_path, 'wb'))


def null_ising(init_lattices, save_cluster = True):
    # model parameters
    num_parallel = len(init_lattices)
    time = 100

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, save_cluster, init_lattice, time) for simulation_index, init_lattice in zip(range(num_parallel), init_lattices)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        save_data(record)


if __name__ == '__main__':
    lattice = randint(0, 2, (4, 100, 100))
    null_ising(lattice, save_cluster=False)