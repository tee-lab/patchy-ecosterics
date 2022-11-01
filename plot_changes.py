from matplotlib import pyplot as plt
from numpy import loadtxt, log, transpose
from os import makedirs, path


def plot_changes(filename):
    output_path = path.join(path.dirname(__file__), "outputs")
    makedirs(output_path, exist_ok=True)

    cluster_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster_growth_probabilities.txt'), 'r')))
    sizes, growth_probabilities = cluster_data[0], cluster_data[1]
    decay_probabilities = 1 - growth_probabilities

    plt.figure()
    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster Size")
    plt.ylabel("Probabilities")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(path.join(output_path, filename + '_cluster_growth_probabilities.png'))
    plt.show()

    changes_data = transpose(loadtxt(open(path.join(output_path, filename + '_changes.txt'), 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

    plt.figure()
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

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.plot(abs_changes, abs_changes_histogram)
    plt.savefig(path.join(output_path, filename + '_changes_abs.png'))
    plt.show()

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities (log-log scale)")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.loglog(abs_changes, abs_changes_histogram)
    plt.savefig(path.join(output_path, filename + '_changes_abs_log_log.png'))
    plt.show()

    cluster_distribution_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster_distribution.txt'), 'r')))
    cluster_sizes, cluster_distribution = cluster_distribution_data[0], cluster_distribution_data[1]

    plt.figure()
    plt.title("Cluster Size Distribution")
    plt.xlabel("Cluster Size")
    plt.ylabel("P(S)")
    plt.plot(cluster_sizes, cluster_distribution)
    plt.savefig(path.join(output_path, filename + '_cluster_distribution.png'))
    plt.show()


if __name__ == '__main__':
    plot_changes("0p71")