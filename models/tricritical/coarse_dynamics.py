from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from multiprocessing import Pool, set_start_method
from numba import njit
from numpy import array, copy, sum, zeros
from numpy.random import random, randint
from pickle import dump
from skimage.measure import label
from tqdm import tqdm
import os

from depth_first_clustering import depth_first_clustering


@njit
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


@njit
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


@njit
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


@njit
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
    simulation_index, length, eq_time, simulation_iters, difference_time, p, q = data
    lattice = randint(0, 2, (length, length))
    lattice = (lattice == 1).astype(int)
    all_changes = zeros((length * length + 1), dtype=(int))

    if simulation_index == 0:
        print("Equilibriating system ...")
        iterator = tqdm(range(eq_time))
    else:
        iterator = range(eq_time)

    for _ in iterator:
        lattice = landscape_update(lattice, p, q)

    if simulation_index == 0:
        print("Simulating cluster dynamics ...")
        iterator = tqdm(range(int(simulation_iters)))
    else:
        iterator = range(int(simulation_iters))

    for _ in iterator:
        old_lattice = copy(lattice)
        for _ in range(difference_time):
            lattice = landscape_update(lattice, p, q)
        new_lattice = copy(lattice)

        difference_map = abs(new_lattice - old_lattice)
        changes_distribution = array(depth_first_clustering(difference_map, periodic=True, trim=False))
        all_changes += changes_distribution

    return all_changes


def tricritical(p_ext = 0.5, q_ext = 0.5, diff_ext = 1, num_parallel = 10):
    # model parameters
    length = 500
    eq_time = 1000
    difference_time = diff_ext
    simulation_iters = 100
    p = p_ext
    q = q_ext

    print(f"\nPreparing {num_parallel} automata in parallel...")
    data = [(simulation_index, length, eq_time, simulation_iters, difference_time, p, q) for simulation_index in range(num_parallel)]
    with Pool(num_parallel) as pool:
        records = list(pool.map(simulate, data))

    all_changes = zeros(length * length + 1, dtype=int)
    for record in records:
        all_changes += record

    cutoff_index = -1
    for i in range(len(all_changes) - 1, -1, -1):
        if all_changes[i] != 0:
            cutoff_index = i + 1
            break

    all_changes = all_changes[1:cutoff_index]
    output_path = os.path.join(os.path.dirname(__file__), "..", "..", "outputs")
    os.makedirs(output_path, exist_ok=True)
    file_name = f"{str(p).replace('.', 'p')}_{difference_time}_diffmap.png"

    plt.figure()
    plt.title("Distribution of patch sizes in difference map")
    plt.xlabel("Patch size")
    plt.ylabel("Number of patches")
    plt.loglog(all_changes)
    plt.savefig(os.path.join(output_path, file_name))


if __name__ == '__main__':
    print(tricritical(0.72, 0.0, 10, 1))