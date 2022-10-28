from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
from os import makedirs, path


def plot_changes(filename):
    output_path = path.join(path.dirname(__file__), "outputs")
    makedirs(output_path, exist_ok=True)

    cluster_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster.txt'), 'r')))
    sizes, growth_probabilities = cluster_data[0], cluster_data[1]
    decay_probabilities = 1 - growth_probabilities

    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster Size")
    plt.ylabel("Probabilities")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(path.join(output_path, filename + '_cluster.png'))
    plt.show()

    changes_data = transpose(loadtxt(open(path.join(output_path, filename + '_changes.txt'), 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

    plt.title("Cluster Change Probabilities")
    plt.xlabel("dS")
    plt.ylabel("P(dS)")
    plt.plot(changes, changes_probabilities)
    plt.savefig(path.join(output_path, filename + '_changes.png'))
    plt.show()

    abs_changes = list(range(0, int(max(max(changes), -min(changes)))))
    abs_changes_histogram = [0] * len(abs_changes)

    for abs_change in abs_changes:
        value = 0

        if abs_change in changes:
            value += changes_probabilities[changes.index(abs_change)]
        if -abs_change in changes:
            value += changes_probabilities[changes.index(-abs_change)]
        
        abs_changes_histogram[abs_change] = value

    abs_changes_histogram[0] = abs_changes_histogram[0] / 2

    plt.title("Cluster Absolute Change Probabilities")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.plot(abs_changes, abs_changes_histogram)
    plt.savefig(path.join(output_path, filename + '_changes_abs.png'))
    plt.show()


if __name__ == '__main__':
    plot_changes("0p67")