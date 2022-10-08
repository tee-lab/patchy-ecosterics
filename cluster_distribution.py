from copy import copy
from matplotlib import pyplot as plt
from numpy import array, log, pad, zeros
from skimage.measure import label

from depth_first_clustering import depth_first_clustering
from linear_regression import perform_linear_regression
from utils import load_automaton_data


def get_probabilities(lattice):
    """ Returns an array such that the i^th element is the probability of that any cluster has area greater than or equal to i """
    final_cluster_sizes = depth_first_clustering(lattice, trim=True)[1:]
    print(f"Clustering completed. {sum(final_cluster_sizes)} clusters found.")
    print(len(final_cluster_sizes))

    cumulative_cluster_sizes = array(copy(final_cluster_sizes), dtype=float)
    for i in range(len(cumulative_cluster_sizes) - 2, -1, -1):
        cumulative_cluster_sizes[i] += cumulative_cluster_sizes[i + 1]
    probabilities = cumulative_cluster_sizes / sum(final_cluster_sizes)

    return probabilities


def trim_log_probabilities(y):
    """ Trims the last few repetitive elements of log_probabilities """
    last_value = y[-1]

    start_index = -1
    for i in range(len(y)):
        if y[i] == last_value:
            start_index = i
            break

    return y[:start_index + 1]


if __name__ == '__main__':
    model = "tricritical"
    simulation_indices = range(0, 10)

    probability_ensembles = []
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Simulation {i + 1} / {len(simulation_indices)}")

        data = load_automaton_data(model, simulation_index)
        time_series, info = data["time_series"], data["info"]

        probabilities = get_probabilities(time_series[-1])
        probability_ensembles.append(probabilities)

    print("Averaging results ...")

    max_length = max([len(ensemble) for ensemble in probability_ensembles])
    averaged_probabilities = zeros(max_length, dtype=float)

    for ensemble in probability_ensembles:
        padded_probabilities = pad(ensemble, (0, max_length - len(ensemble)), mode="constant", constant_values=0)
        averaged_probabilities += padded_probabilities

    averaged_probabilities /= len(probability_ensembles)
    log_probabilities = trim_log_probabilities(log(averaged_probabilities))
    log_sizes = log(range(1, len(log_probabilities) + 1))

    print("Fitting line ...")
    beta, c, r_squared = perform_linear_regression(log_sizes, log_probabilities)

    plt.title(info)
    plt.xlabel("log of Cluster sizes")
    plt.ylabel("log P(A >= a)")
    plt.plot(log_sizes, log_probabilities, 'o', markersize=2)
    plt.plot(log_sizes, beta * log_sizes + c)
    plt.legend([f'Averaged data of {len(probability_ensembles)} simulations', f'Power-law fit with beta = {-beta:.3f}, R2 = {r_squared:.3f}'])
    plt.show()