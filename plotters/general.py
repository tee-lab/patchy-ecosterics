from matplotlib import pyplot as plt
from numpy import loadtxt, transpose, zeros
from os import path


def plot_growth_probabilities(folder, file_prefix):
    filename = file_prefix + "_cluster_growth_probabilities.txt"
    cluster_data = transpose(loadtxt(open(path.join(folder, filename), 'r')))
    sizes, growth_probabilities = cluster_data[0], cluster_data[1]
    decay_probabilities = 1 - growth_probabilities

    plt.figure()
    plt.title("Cluster Growth and Decay Probabilities")
    plt.xlabel("Cluster Size")
    plt.ylabel("Probabilities")
    plt.plot(sizes, growth_probabilities, label="Growth")
    plt.plot(sizes, decay_probabilities, label="Decay")
    plt.legend()
    plt.savefig(path.join(folder, file_prefix + '_cluster_growth_probabilities.png'))
    plt.show()


def plot_sde(folder, file_prefix, limit):
    filename = file_prefix + "_cluster_ds.txt"
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, filename), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[:, :cluster_analyze_limit]

    plt.figure()
    plt.title("Mean Cluster Change")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS")
    plt.plot(range(cluster_analyze_limit), cluster_ds_data[1])
    plt.plot(range(cluster_analyze_limit), [0 for _ in range(cluster_analyze_limit)])
    plt.savefig(path.join(folder, file_prefix + '_cluster_mean_ds.png'))
    plt.show()

    plt.figure()
    plt.title("Mean Cluster Change Squared")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS^2")
    plt.plot(range(cluster_analyze_limit), cluster_ds_data[2])
    plt.savefig(path.join(folder, file_prefix + '_cluster_mean_ds_sq.png'))
    plt.show()

    plt.figure()
    plt.title("Number of Cluster Changes")
    plt.xlabel("Cluster Size")
    plt.ylabel("Number of Changes")
    plt.plot(range(cluster_analyze_limit), cluster_ds_data[3])
    plt.savefig(path.join(folder, file_prefix + '_cluster_num_changes.png'))
    plt.show()


def plot_cluster_distribution(folder, file_prefix):
    filename = file_prefix + "_cluster_distribution.txt"
    cluster_distribution_data = transpose(loadtxt(open(path.join(folder, filename), 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))

    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:]) / sum(num)

    plt.figure()
    plt.title("Cluster Size Distribution (log-log scale)")
    plt.xlabel("Cluster Size")
    plt.ylabel("Inverse CDF")
    plt.loglog(cluster_sizes, inverse_cdf, 'o')
    plt.savefig(path.join(folder, file_prefix + '_cluster_distribution_log_log.png'))
    plt.show()


def plot_cluster_dynamics(folder, file_prefix):
    filename = file_prefix + "_changes.txt"
    changes_data = transpose(loadtxt(open(path.join(folder, filename), 'r')))
    changes, changes_histogram = list(changes_data[0]), changes_data[1]
    changes_probabilities = changes_histogram / sum(changes_histogram)

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
    plt.savefig(path.join(folder, file_prefix + '_changes_abs_log_log.png'))
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
    plt.savefig(path.join(folder, file_prefix + '_changes_abs_log_log_inverse_cdf.png'))
    plt.show()

if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    p = 0.72
    q = 0
    dataset = "100x100"

    folder = "q" + str(q).replace('.', 'p')
    subfolder = str(p).replace('.', 'p')
    data_path = path.join(results_path, model, folder, dataset, subfolder)

    # plot_growth_probabilities(data_path, subfolder)
    # plot_sde(data_path, subfolder, 2000)
    # plot_cluster_distribution(data_path, subfolder)
    plot_cluster_dynamics(data_path, subfolder)