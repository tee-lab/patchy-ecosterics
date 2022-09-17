from matplotlib import pyplot as plt
from numpy import histogram
from skimage.measure import label

from cluster_tracking import get_cluster_size, get_num_active, get_num_clusters
from utils import load_automaton_data


def update_distribution(distribution, cluster_size):
    while len(distribution) < cluster_size + 1:
        distribution.append(0)

    distribution[cluster_size] += 1    


def get_all_cluster_sizes(lattice):
    labelled_lattice = label(lattice)
    num_clusters = labelled_lattice.max()

    cluster_sizes = []
    for i in range(1, num_clusters):
        cluster_size = get_cluster_size(labelled_lattice, i)
        cluster_sizes.append(cluster_size)

    return cluster_sizes


if __name__ == '__main__':
    data = load_automaton_data("scanlon_kalahari", 0)
    time_series, info = data["time_series"], data["info"]

    cluster_sizes = get_all_cluster_sizes(time_series[-1])
    cluster_histogram = list(histogram(cluster_sizes, bins=range(1, max(cluster_sizes) + 1)))

    plt.plot(cluster_histogram, range(1, max(cluster_sizes) + 1))
    plt.show()