from matplotlib import pyplot as plt
from numpy import loadtxt, log, transpose, zeros
from os import makedirs, path


def trim_log_probabilities(y):
    """ Trims the last few repetitive elements of log_probabilities """
    last_value = y[-1]

    start_index = -1
    for i in range(len(y)):
        if y[i] == last_value:
            start_index = i
            break

    return y[:start_index + 1]


def plot_changes(filename, base_path = "outputs"):
    output_path = path.join(path.dirname(__file__), base_path)
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

    cluster_ds_data = open(path.join(output_path, filename + '_cluster_ds.txt'), 'r').readlines()
    cluster_analyze_limit = 200
    mean_ds_values, mean_ds_sq_values, num_changes = zeros(cluster_analyze_limit), zeros(cluster_analyze_limit), zeros(cluster_analyze_limit)

    for i, line in enumerate(cluster_ds_data):
        cluster_size, ds_values = line.split(":")

        if int(cluster_size) == cluster_analyze_limit or ds_values == " \n":
            break

        ds_values = [int(ds) for ds in ds_values.strip().split(" ")]
        ds_sq_values = [ds ** 2 for ds in ds_values]
        mean_ds_values[i] = sum(ds_values) / len(ds_values)
        mean_ds_sq_values[i] = sum(ds_sq_values) / len(ds_sq_values)
        num_changes[i] = len(ds_values)

    plt.figure()
    plt.title("Mean Cluster Change")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS")
    plt.plot(range(cluster_analyze_limit), mean_ds_values)
    plt.savefig(path.join(output_path, filename + '_cluster_mean_ds.png'))
    plt.show()

    plt.figure()
    plt.title("Mean Cluster Change Squared")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS^2")
    plt.plot(range(cluster_analyze_limit), mean_ds_sq_values)
    plt.savefig(path.join(output_path, filename + '_cluster_mean_ds_sq.png'))
    plt.show()

    plt.figure()
    plt.title("Number of Cluster Changes")
    plt.xlabel("Cluster Size")
    plt.ylabel("Number of Changes")
    plt.plot(range(cluster_analyze_limit), num_changes)
    plt.savefig(path.join(output_path, filename + '_cluster_num_changes.png'))
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
    plt.title("Cluster Absolute Change Probabilities (log-log scale)")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.loglog(abs_changes[3:], abs_changes_histogram[3:])
    plt.savefig(path.join(output_path, filename + '_changes_abs_log_log.png'))
    plt.show()

    probability = zeros(len(abs_changes_histogram))
    probability[0] = sum(abs_changes_histogram)

    for i in range(1, len(abs_changes_histogram)):
        probability[i] = probability[i - 1] - abs_changes_histogram[i - 1]

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities (log-log scale)")
    plt.xlabel("|dS|")
    plt.ylabel("Inverse CDF")
    plt.loglog(abs_changes[3:], probability[3:])
    plt.savefig(path.join(output_path, filename + '_changes_abs_log_log_inverse_cdf.png'))
    plt.show()

    cluster_distribution_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster_distribution.txt'), 'r')))
    cluster_sizes, cluster_distribution = cluster_distribution_data[0], cluster_distribution_data[1]

    probability = zeros(len(cluster_distribution))
    probability[0] = sum(cluster_distribution)

    for i in range(1, len(cluster_distribution)):
        probability[i] = probability[i - 1] - cluster_distribution[i - 1]

    plt.figure()
    plt.title("Cluster Size Distribution (log-log scale)")
    plt.xlabel("Cluster Size")
    plt.ylabel("Inverse CDF")
    plt.loglog(cluster_sizes, probability, 'o')
    plt.savefig(path.join(output_path, filename + '_cluster_distribution_log_log.png'))
    plt.show()


if __name__ == '__main__':
    # modified_base_path = path.join("results", "tricritical", "q0", "alternate", "0p74")
    modified_base_path = path.join("results", "null_stochastic", "0p6")
    plot_changes("0p6", modified_base_path)