from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros
from os import path
from tqdm import tqdm


def get_cluster_distribution(data_path, folder, file_name):
    file_path = path.join(data_path, folder, file_name)
    cluster_distribution_data = transpose(loadtxt(open(file_path, 'r')))
    cluster_sizes, num = cluster_distribution_data[0][1:], cluster_distribution_data[1][1:]

    inverse_cdf = zeros(len(num))
    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:])
    inverse_cdf = inverse_cdf / sum(num)

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if inverse_cdf[i] == inverse_cdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    inverse_cdf = delete(inverse_cdf, remove_indices)

    return cluster_sizes, inverse_cdf


def get_cluster_dynamics(data_path, folder, file_name):
    file_path = path.join(data_path, folder, file_name)
    changes_data = transpose(loadtxt(open(file_path, 'r')))
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

    return abs_changes[3:], inverse_cdf[3:]


def get_mean_ds(data_path, name, limit):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[1]

    return range(cluster_analyze_limit), cluster_ds_data[:cluster_analyze_limit]


def get_mean_ds_sq(data_path, name, limit):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[2]

    return range(cluster_analyze_limit), cluster_ds_data[:cluster_analyze_limit]


if __name__ == '__main__':
    root_path = path.join(path.dirname(__file__), "..")
    dataset = "100x100"

    # q = 0
    # p_values = [0.65, 0.7, 0.72, 0.74]
    # densities = [0.27, 0.48, 0.54, 0.61]
    # tdp_cluster_limits = [100, 500, 4000, 6000]
    # null_cluster_limits = [50, 250, 2000, 6000]
    
    # q = 0.25
    # p_values = [0.6, 0.62, 0.65, 0.67]
    # densities = [0.35, 0.45, 0.55, 0.61]
    # tdp_cluster_limits = [100, 500, 4000, 6000]
    # null_cluster_limits = [50, 250, 2000, 6000]

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]
    # densities = [0.06, 0.43, 0.53, 0.6]
    # tdp_cluster_limits = [100, 500, 4000, 6000]
    # null_cluster_limits = [50, 200, 1500, 6000]

    # q = 0.75
    # p_values = [0.405, 0.41, 0.42, 0.44]
    # densities = [0.23, 0.38, 0.52, 0.64]
    # tdp_cluster_limits = [200, 1000, 4000, 6000]
    # null_cluster_limits = [25, 150, 1000, 6000]

    q = 0.92
    p_values = [0.282, 0.283, 0.285, 0.29]
    densities = [0.09, 0.17, 0.4, 0.7]
    tdp_cluster_limits = [300, 1000, 4000, 6000]
    null_cluster_limits = [10, 25, 50, 6000]

    assert len(p_values) == len(densities) == len(tdp_cluster_limits)

    title_size = 16
    label_size = 14

    q_folder = "q" + str(q).replace(".", "p") 
    null_path = path.join("results", "null_stochastic")
    tdp_path = path.join("results", "tricritical", q_folder, dataset)

    plt.subplots(4, len(p_values), figsize=(40, 26))
    for i in tqdm(range(len(p_values))):
        col = i + 1
        p = p_values[i]
        density = densities[i]

        tdp_folder = str(p).replace(".", "p")
        null_folder = str(density).replace(".", "p")

        row = 1
        tdp_file_name = tdp_folder + "_cluster_distribution.txt"
        tdp_cluster_sizes, tdp_inverse_cdf = get_cluster_distribution(tdp_path, tdp_folder, tdp_file_name)
        null_file_name = null_folder + "_cluster_distribution.txt"
        null_cluster_sizes, null_inverse_cdf = get_cluster_distribution(null_path, null_folder, null_file_name)

        plt.subplot(4, len(p_values), col)
        plt.title("Cluster Size Distribution", fontsize=title_size)
        plt.xlabel("s", fontsize=label_size)
        if col == 1:
            plt.ylabel("P(S > s)", fontsize=label_size)
        plt.loglog(tdp_cluster_sizes, tdp_inverse_cdf, 'o', label="TDP")
        plt.loglog(null_cluster_sizes, null_inverse_cdf, 'o', label="Null")
        plt.legend()

        row = 2
        tdp_file_name = tdp_folder + "_changes.txt"
        tdp_changes, tdp_inverse_cdf = get_cluster_dynamics(tdp_path, tdp_folder, tdp_file_name)
        null_file_name = null_folder + "_changes.txt"
        null_changes, null_inverse_cdf = get_cluster_dynamics(null_path, null_folder, null_file_name)

        plt.subplot(4, len(p_values), col + len(p_values))
        plt.title("Cluster Dynamics", fontsize=title_size)
        plt.xlabel("ds", fontsize=label_size)
        if col == 1:
            plt.ylabel("P(dS > ds)", fontsize=label_size)
        plt.loglog(tdp_changes, tdp_inverse_cdf, label="TDP")
        plt.loglog(null_changes, null_inverse_cdf, label="Null")
        plt.legend()

        row = 3
        tdp_file_name = tdp_folder + "_cluster_ds.txt"
        tdp_cluster_sizes, tdp_cluster_ds = get_mean_ds(tdp_path, tdp_folder, tdp_cluster_limits[i])
        null_file_name = null_folder + "_cluster_ds.txt"
        null_cluster_sizes, null_cluster_ds = get_mean_ds(null_path, null_folder, null_cluster_limits[i])

        plt.subplot(4, len(p_values), col + 2 * len(p_values))
        plt.title("Drift Term", fontsize=title_size)
        plt.xlabel("s", fontsize=label_size)
        if col == 1:
            plt.ylabel("Mean ds", fontsize=label_size)
        plt.plot(tdp_cluster_sizes, tdp_cluster_ds, label="TDP")
        plt.plot(null_cluster_sizes, null_cluster_ds, label="Null")
        plt.plot([0, max(tdp_cluster_limits[i], null_cluster_limits[i])], [0, 0], 'k--')
        plt.legend()

        row = 4
        tdp_file_name = tdp_folder + "_cluster_ds.txt"
        tdp_cluster_sizes, tdp_cluster_ds_sq = get_mean_ds_sq(tdp_path, tdp_folder, tdp_cluster_limits[i])
        null_file_name = null_folder + "_cluster_ds.txt"
        null_cluster_sizes, null_cluster_ds_sq = get_mean_ds_sq(null_path, null_folder, null_cluster_limits[i])

        plt.subplot(4, len(p_values), col + 3 * len(p_values))
        plt.title("Diffusion Term", fontsize=title_size)
        plt.xlabel("s", fontsize=label_size)
        if col == 1:
            plt.ylabel("Mean (ds^2)", fontsize=label_size)
        plt.plot(tdp_cluster_sizes, tdp_cluster_ds_sq, label="TDP")
        plt.plot(null_cluster_sizes, null_cluster_ds_sq, label="Null")
        plt.legend()

    plt.savefig(f"q{str(q).replace('.', 'p')}_null.png", bbox_inches='tight')
    plt.show()