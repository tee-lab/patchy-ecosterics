from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from itertools import product
from numba import njit
from numpy import array, sum, zeros
from random import randint, random


@njit(nogil=True, fastmath=True)
def balance_automaton(lattice, required_occupancy):
    while True:
        current_occupancy = sum(lattice) / (length * length)

        if abs(current_occupancy - required_occupancy) < tolerance:
            break
        else:
            i = randint(0, length - 1)
            j = randint(0, length - 1)

            if current_occupancy < required_occupancy:
                while lattice[i, j] != 0:
                    i = randint(0, length - 1)
                    j = randint(0, length - 1)
                lattice[i, j] = 1
            else:
                while lattice[i, j] != 1:
                    i = randint(0, length - 1)
                    j = randint(0, length - 1)
                lattice[i, j] = 0

    return lattice

def generate_automaton(required_occupancy):
    lattice = zeros((length, length), dtype=int)
    for i, j in product(range(length), range(length)):
        if random() < required_occupancy:
            lattice[i, j] = 1

    balance_automaton(lattice, required_occupancy)
    return lattice


def null(occupancy, tol, num_parallel=10):
    global length, tolerance, required_occupancy
    length = 1000
    tolerance = max(tol, 1.0 / (length * length))

    with ThreadPoolExecutor(max_workers=num_parallel) as pool:
        lattice_record = list(pool.map(generate_automaton, [occupancy for _ in range(num_parallel)]))

    return lattice_record


if __name__ == '__main__':
    null(0.8, 0.01)