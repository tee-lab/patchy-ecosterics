from matplotlib import pyplot as plt
from numpy import loadtxt, transpose


def plot_changes(filename):
    cluster_data = transpose(loadtxt(open(filename + '_cluster.txt', 'r')))
    sizes, growth_probabilities = cluster_data[0], cluster_data[1]
    decay_probabilities = 1 - growth_probabilities

    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster Size")
    plt.ylabel("Probabilities")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(filename + '_cluster.png')
    plt.show()

    changes_data = transpose(loadtxt(open(filename + '_changes.txt', 'r')))
    changes, changes_histogram= changes_data[0], changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

    plt.title("Cluster Change Probabilities")
    plt.xlabel("dS")
    plt.ylabel("P(dS)")
    plt.plot(changes, changes_probabilities)
    plt.savefig(filename + '_changes.png')
    plt.show()

    abs_changes = list(range(0, max(max(changes), -min(changes))))
    abs_changes_histogram = [0] * len(abs_changes)

    for abs_change in abs_changes:
        pos_index = changes.index(abs_change)
        neg_index = changes.index(-abs_change)
        abs_changes_histogram[abs_change] = changes_histogram[pos_index] + changes_histogram[neg_index]
    abs_changes_histogram[0] = abs_changes_histogram[0] / 2

    plt.title("Cluster Absolute Change Probabilities")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.plot(abs_changes, abs_changes_histogram)
    plt.savefig(filename + '_abs_changes.png')
    plt.show()