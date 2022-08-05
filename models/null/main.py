from concurrent.futures import ThreadPoolExecutor
from matplotlib import pyplot as plt
from numba import njit
from numpy import sum, zeros
from random import randint, random


def generate_automaton(required_occupancy):
    lattice = zeros((length, length), dtype=int)

    for i in range(length):
        for j in range(length):
            if random() < required_occupancy:
                lattice[i, j] = 1

    while True:
        current_occupancy = sum(lattice) / (length * length)

        if abs(current_occupancy - required_occupancy) < tolerance:
            break
        else:
            i = randint(0, length - 1)
            j = randint(0, length - 1)

            if current_occupancy < required_occupancy:
                lattice[i, j] == 1
            else:
                lattice[i, j] == 0

    return lattice


def null(occupancy, tol, num_parallel=10):
    global length, tolerance
    length = 100
    tolerance = max(tol, 1.0 / (length * length))

    with ThreadPoolExecutor(max_workers=num_parallel) as pool:
        lattice_record = list(pool.map(generate_automaton, [occupancy] * num_parallel))

    return lattice_record


if __name__ == '__main__':
    null(0.5, 0.01)