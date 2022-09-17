from concurrent.futures import ThreadPoolExecutor
from math import floor, sqrt
from numba import njit
from numpy import array, copy, sum
from numpy.random import randint
from pickle import dump
from random import random

import os


@njit(nogil=True, fastmath=True)
def mc_step(lattice, f_carrying):
    """ Simulates a single mc step on the lattice """
    f_current = sum(lattice) / (length * length)

    for _ in range(mc_updates):
        i = int(random() * length)
        j = int(random() * length)
        rho = get_positive_feedback(lattice, i, j)

        if lattice[i, j] == 0:
            prob_growth = rho + (f_carrying - f_current) / (1 - f_current)
            if random() < prob_growth:
                lattice[i, j] = 1
                f_current += 1 / (length * length)
        else:
            prob_decay = (1 - rho) + (f_current - f_carrying) / f_current
            if random() < prob_decay:
                lattice[i, j] = 0
                f_current -= 1 / (length * length)


@njit(nogil=True, fastmath=True)
def get_positive_feedback(lattice, i, j):
    """ Calculates the positive feedback operating at (i, j) """
    density = 0
    normalization = 0

    for a in range(i - r_influence, i + r_influence + 1):
        for b in range(j - r_influence, j + r_influence + 1):
            distance = sqrt((i - a) ** 2 + (j - b) ** 2)
            if 0 <= a < length and 0 <= b < length and distance < r_influence:
                weight_term = 1 - (distance / immediacy)
                density += weight_term * lattice[a, b]
                normalization += weight_term

    return (density / normalization)


def simulate(simulation_index):
    # initialize lattice and time series
    lattice = randint(0, 2, (length, length))
    time_series = [copy(lattice)]

    if simulation_index == 0:
        print("Compiling functions...")

    # simulate
    for i in range(mc_steps):
        mc_step(lattice, f_carrying)
        time_series.append(copy(lattice))

        if simulation_index == 0:
            print(f"{i * 100 / mc_steps} %", end="\r")

    return time_series


def get_forest_cover(rainfall):
    """ Calculates the forest cover for a given value of rainfall, based on a linear fit """
    slope = 0.0008588
    intercept = -0.1702

    return max(slope * rainfall + intercept, 0)


def save_automaton_data(time_series):
    """ Saves the entire simulation data in a pickle file, in the same folder """
    current_path = os.path.dirname(__file__)
    files_list = os.listdir(current_path)

    num_automaton_simulations = 0
    for file_name in files_list:
        if file_name.startswith("simulation_") and file_name.endswith(".pkl"):
            num_automaton_simulations += 1

    file_name = 'simulation_{}.pkl'.format(num_automaton_simulations)
    save_path = os.path.join(current_path, file_name)
    info_string = f"Scanlon Kalahari with rainfall: {rainfall} mm\n"

    automaton_data = {}
    automaton_data["time_series"] = array(time_series, dtype=bool)
    automaton_data["info"] = info_string
    dump(automaton_data, open(save_path, 'wb'))

    info_path = os.path.join(current_path, "info.txt")
    with open(info_path, 'a') as info_file:
        info_file.write(info_string)


def scanlon_kalahari(rainfall_ext = 800, num_parallel = 10, save = False):
    # model parameters
    global length, rainfall, f_carrying, r_influence, immediacy
    length = 100
    rainfall = rainfall_ext
    f_carrying = get_forest_cover(rainfall)
    r_influence = 6
    immediacy = 24

    # simulation parameters
    global mc_steps, mc_updates
    mc_steps = 200
    mc_updates = floor(0.2 * length * length)

    print(f"Simulating {num_parallel} automatons in parallel ...")
    with ThreadPoolExecutor(7) as pool:
        time_series_records = list(pool.map(simulate, range(num_parallel)))

    if save:
        print("Saving data...")
        for time_series in time_series_records:
            save_automaton_data(time_series)

    avg_final_density = 0
    for time_series in time_series_records:
        avg_final_density += sum(time_series[-1]) / (length * length)
    avg_final_density /= num_parallel

    return avg_final_density


if __name__ == '__main__':
    scanlon_kalahari(800, 1, True)