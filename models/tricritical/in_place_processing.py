from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool, set_start_method
from numpy import array, copy, sum
from numpy.random import random, randint
from pickle import dump
from skimage.measure import label
from tqdm import tqdm
import os

from cluster_dynamics import get_cluster_dynamics, get_changed_lattice


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


def simulate(data):
    simulation_index, save_series, save_cluster, length, eq_time, simulation_time, p, q = data
    lattice = randint(0, 2, (length, length))
    lattice = (lattice == 1).astype(int)

    density_data = []
    series_data = []
    cluster_data = []

    if simulation_index == 0:
        print("Equilibriating system ...")
        iterator = tqdm(range(eq_time))
    else:
        iterator = range(eq_time)

    for i in iterator: 
        lattice = landscape_update(lattice, p, q)

        # save density and series data
        density_data.append(sum(lattice) / (length * length))
        if save_series:
            series_data.append(copy(lattice))

    if simulation_index == 0:
        print("Simulating cluster dynamics ...")
        iterator = tqdm(range(int(simulation_time * length * length)))
    else:
        iterator = range(int(simulation_time * length * length))

    old_labels = label(lattice, background=0, connectivity=1)
    new_labels = None

    for i in iterator:
        # single update
        lattice, changed_coords = single_update(lattice, p, q)

        # save cluster data
        if save_cluster:
            if changed_coords is None:
                cluster_data.append(None)
            else:
                new_labels = get_changed_lattice(old_labels, changed_coords)
                status = get_cluster_dynamics(old_labels, new_labels, changed_coords)
                cluster_data.append(status)
                old_labels = new_labels.copy()

        # periodic saving of series and density data
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


def save_data(data):
    record, p, q, simulation_index = data
    """ Saves the entire simulation data in a pickle file, in the same folder """
    current_path = os.path.dirname(__file__)

    file_name = f"simulation_{simulation_index}.pkl"
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


def tricritical(p_ext = 0.5, q_ext = 0.5, num_parallel = 10, save_series = False, save_cluster = False):
    # model parameters
    length = 100
    eq_time = 200
    simulation_time = 1000
    p = p_ext
    q = q_ext

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, save_series, save_cluster, length, eq_time, simulation_time, p, q) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    print("Saving data ...")
    data = [(record, p, q, simulation_index) for simulation_index, record in enumerate(records)]
    with ThreadPoolExecutor(num_parallel) as executor:
        executor.map(save_data, data)

    avg_final_density = 0
    for record in records:
        density_data, _, _, _ = record
        avg_final_density += density_data[-1]
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    print(tricritical(0.72, 0.0, 7, save_series=True, save_cluster=True))