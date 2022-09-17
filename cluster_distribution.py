from matplotlib import pyplot as plt
from numba import njit
from numpy import array, exp, log, pad, zeros
from skimage.measure import label
from sklearn.linear_model import LinearRegression

from cluster_tracking import get_cluster_size
from linear_regression import perform_linear_regression
from utils import load_automaton_data


@njit
def get_cdf(cluster_sizes):
    num_clusters = len(cluster_sizes)
    cdf = []

    for size in range(1, max(cluster_sizes) + 1):
        probability = 0
        for cluster_size in cluster_sizes:
            if cluster_size >= size:
                probability += 1
        probability /= num_clusters
        cdf.append(probability)

    truncate_index = cdf.index(min(cdf))

    return cdf[:truncate_index]


def get_all_cluster_sizes(lattice):
    labelled_lattice = label(lattice, background=1)
    num_clusters = labelled_lattice.max()

    cluster_sizes = []
    for i in range(1, num_clusters):
        cluster_size = get_cluster_size(labelled_lattice, i)
        cluster_sizes.append(cluster_size)

    return cluster_sizes


if __name__ == '__main__':
    model = "tricritical"
    simulation_indices = range(0, 10)

    print("Computing CDFs ...")

    probability_ensembles = []
    for i, simulation_index in enumerate(simulation_indices):
        print(f"Simulation {i + 1} / {len(simulation_indices)}")

        data = load_automaton_data(model, simulation_index)
        time_series, info = data["time_series"], data["info"]

        cluster_sizes = array(get_all_cluster_sizes(time_series[-1]), dtype=int)
        probabilities = get_cdf(cluster_sizes)
        probability_ensembles.append(probabilities)

    print("Averaging results ...")

    max_length = max([len(ensemble) for ensemble in probability_ensembles])
    averaged_probabilities = zeros(max_length, dtype=float)

    for ensemble in probability_ensembles:
        padded_probabilities = pad(ensemble, (0, max_length - len(ensemble)), mode="constant", constant_values=0)
        averaged_probabilities += padded_probabilities

    averaged_probabilities /= len(probability_ensembles)
    sizes = array(list(range(1, len(averaged_probabilities) + 1)))

    log_probabilities = log(averaged_probabilities)
    log_sizes = log(sizes)

    print("Fitting line ...")
    beta, c, r_squared = perform_linear_regression(log_sizes, log_probabilities)

    plt.title(info)
    plt.xlabel("Cluster sizes")
    plt.ylabel("P(A >= a)")
    plt.plot(log_sizes, log_probabilities, 'o')
    plt.plot(log_sizes, beta * log_sizes + c)
    plt.legend([f'Averaged data of {len(probability_ensembles)} simulations', f'Power-law fit with beta = {-beta:.3f}'])
    plt.show()