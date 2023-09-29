"""
Processes all the .txt files crunced by compile_changes.py file to generate plots
"""


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


def plot_changes(filename, base_path = "outputs", calc_residue=False):
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
    plt.close()

    cluster_ds_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = len(cluster_ds_data[0])
    cluster_ds_data = cluster_ds_data[:, :cluster_analyze_limit]

    num_cutoff = 10000
    sde_cutoff = -1
    
    for i in range(1, len(cluster_ds_data[3])):
        if cluster_ds_data[3][i] < num_cutoff:
            sde_cutoff = i
            break

    if sde_cutoff == -1:
        sde_cutoff = len(cluster_ds_data[3])

    print(sde_cutoff)

    plt.figure()
    plt.title("Mean Cluster Change")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS")
    plt.plot(range(sde_cutoff), cluster_ds_data[1][:sde_cutoff])
    plt.plot(range(sde_cutoff), [0 for _ in range(sde_cutoff)])
    plt.savefig(path.join(output_path, filename + '_cluster_mean_ds.png'))
    plt.show()
    plt.close()

    plt.figure()
    plt.title("Mean Cluster Change Squared")
    plt.xlabel("Cluster Size")
    plt.ylabel("Mean dS^2")
    plt.plot(range(sde_cutoff), cluster_ds_data[2][:sde_cutoff])
    plt.savefig(path.join(output_path, filename + '_cluster_mean_ds_sq.png'))
    plt.show()
    plt.close()

    plt.figure()
    plt.title("Number of Cluster Changes")
    plt.xlabel("Cluster Size")
    plt.ylabel("Number of Changes")
    plt.plot(range(cluster_analyze_limit), cluster_ds_data[3])
    plt.savefig(path.join(output_path, filename + '_cluster_num_changes.png'))
    plt.show()
    plt.close()

    if calc_residue:
        residue_data = open(path.join(output_path, filename + '_residue_info.txt'), 'r').read().split('\n')
        for data in residue_data[:-1]:
            size, bins, freq = data.split(':')
            min_bin, max_bin = bins.split(',')
            freqs = list(map(int, freq.split(',')))

            plt.figure()
            plt.title("Residue distribution for cluster size " + size)
            plt.xlabel("Residue")
            plt.ylabel("Frequency")
            plt.bar(range(int(min_bin), int(max_bin)), freqs)
            plt.savefig(path.join(output_path, filename + '_residue_' + size[:-1] + '.png'))

    changes_data = transpose(loadtxt(open(path.join(output_path, filename + '_changes.txt'), 'r')))
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

    probability_distribution = abs_changes_histogram / sum(abs_changes_histogram)
    inverse_cdf = zeros(len(probability_distribution))
    for i in range(len(probability_distribution)):
        inverse_cdf[i] = sum(probability_distribution[i:])
    inverse_cdf = inverse_cdf / sum(inverse_cdf)

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities (log-log scale)")
    plt.xlabel("|dS|")
    plt.ylabel("P(|dS|)")
    plt.loglog(abs_changes[3:], abs_changes_histogram[3:])
    plt.savefig(path.join(output_path, filename + '_changes_abs_log_log.png'))
    plt.show()
    plt.close()

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities (log-log scale)")
    plt.xlabel("|dS|")
    plt.ylabel("Inverse CDF")
    plt.loglog(abs_changes[3:], inverse_cdf[3:])
    plt.savefig(path.join(output_path, filename + '_changes_abs_log_log_inverse_cdf.png'))
    plt.show()
    plt.close()

    plt.figure()
    plt.title("Cluster Absolute Change Probabilities (semilogy scale)")
    plt.xlabel("|dS|")
    plt.ylabel("Inverse CDF")
    plt.semilogy(abs_changes[3:], inverse_cdf[3:])
    plt.savefig(path.join(output_path, filename + '_changes_abs_semilogy_inverse_cdf.png'))
    plt.show()
    plt.close()

    cluster_distribution_data = transpose(loadtxt(open(path.join(output_path, filename + '_cluster_distribution.txt'), 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))
    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:])
    inverse_cdf = inverse_cdf / sum(inverse_cdf)

    plt.figure()
    plt.title("Cluster Size Distribution (log-log scale)")
    plt.xlabel("Cluster Size")
    plt.ylabel("Inverse CDF")
    plt.loglog(cluster_sizes, inverse_cdf, 'o')
    plt.savefig(path.join(output_path, filename + '_cluster_distribution_log_log.png'))
    plt.show()
    plt.close()


if __name__ == '__main__':
    modified_base_path = path.join("results", "tricritical", "q0", "100x100_residue", "0p72")
    plot_changes("0p72", modified_base_path)