from math import exp
from multiprocessing import Pool
from numpy import array, copy, sum, zeros
from numpy.random import random, randint
from pickle import dump
from skimage.measure import label
from tqdm import tqdm
import os

from cluster_dynamics import get_cluster_dynamics, get_changed_lattice


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
    simulation_index, save_series, save_cluster, fractional_cover, length, eq_time, simul_time = data

    lattice = get_init_lattice(length, fractional_cover)

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

    density_data = []
    cluster_data = []
    series_data = []

    if simulation_index == 0:
        iterator = tqdm(range(eq_time))
    else:
        iterator = range(eq_time)

    for i in iterator:
        lattice = landscape_update(lattice, r, m)
        density_data.append(sum(lattice) / (length * length))

        if save_series:
            series_data.append(copy(lattice))

    if simulation_index == 0:
        iterator = tqdm(range(int(simul_time * length * length)))
    else:
        iterator = range(int(simul_time * length * length))

    old_labels = label(lattice, background=0, connectivity=1)
    new_labels = None

    for i in iterator:
        # single update
        lattice, changed_coords = single_update(lattice, r, m)

        # save cluster data
        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                new_labels = get_changed_lattice(old_labels, changed_coords)
                status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
                cluster_data.append(status)
                old_labels = new_labels.copy()

        # periodic saving of density and series data
        if (i % (length * length)) == 0:
            density_data.append(sum(lattice) / (length * length))
            if save_series:
                series_data.append(copy(lattice))

    if len(series_data) == 1:
        series_data = None
    if cluster_data == []:
        cluster_data = None

    records = [density_data, cluster_data, series_data, lattice]
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
    info_string = f"Null Stochastic model\n"

    # save everything available
    data = {}
    density_data, cluster_data, series_data, final_lattice = record
    data["info"] = info_string
    data["density_data"] = density_data
    data["final_lattice"] = final_lattice
    data["series_data"] = series_data
    data["cluster_data"] = cluster_data
    
    dump(data, open(save_path, 'wb'))


def null_stochastic(fractional_cover, num_parallel = 10, save_series = False, save_cluster = True):
    # model parameters
    length = 100
    eq_time = 100
    simul_time = 1000

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster, fractional_cover, length, eq_time, simul_time) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data...")
    for record in records:
        save_data(record)


if __name__ == '__main__':
    null_stochastic(0.5, num_parallel=4, save_cluster=False)