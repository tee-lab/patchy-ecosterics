from matplotlib import pyplot as plt
from numba import njit
from numpy import sum

from utils import load_automaton_data


@njit(nogil=True, fastmath=True)
def cluster_coefficient(lattice):
    length = len(lattice[0])
    rho_p = sum(lattice) / (length * length)

    num_pairs = 0
    for i in range(length):
        for j in range(length - 1):
            if lattice[i, j] == 1 and lattice[i, j + 1] == 1:
                num_pairs += 1

    for j in range(length):
        for i in range(length - 1):
            if lattice[i, j] == 1 and lattice[i + 1, j] == 1:
                num_pairs += 1

    rho_pp = num_pairs / (length * length)

    return rho_pp / (rho_p * rho_p)


def plot_cluster_coefficient(model_name, simulation_indices):
    """ Plots the time variation of cluster coefficient """

    records = []
    for simulation_index in simulation_indices:
        automaton_data = load_automaton_data(model_name, simulation_index)
        time_series, info_string = automaton_data["time_series"], automaton_data["info"]

        cluster_coeffs = [cluster_coefficient(lattice) for lattice in time_series]
        records.append(cluster_coeffs)

    length_records = len(records[0])
    num_records = len(records)

    avg_cluster_coeffs = []
    for i in range(length_records):
        avg_cluster_coeffs.append(sum([record[i] for record in records]) / num_records)

    plt.title(f"Variation of cluster coefficient for " + info_string)
    plt.plot(range(length_records), avg_cluster_coeffs)
    plt.show()


if __name__ == '__main__':
    plot_cluster_coefficient("scanlon_kalahari", range(8))