from matplotlib import pyplot as plt
from numpy import arange, delete, loadtxt, transpose, zeros
from os import path
from tqdm import tqdm


def get_tricritical_phase_diagram(phase_diagram_path, q_value):
    file_path = path.join(phase_diagram_path, "phase_diagram.txt")
    phase_diagram_data = transpose(loadtxt(open(file_path, 'r')))

    p, q, value = phase_diagram_data[0], phase_diagram_data[1], phase_diagram_data[2]
    p_values = []
    densities = []

    for i in range(len(p)):
        if q[i] == q_value:
            p_values.append(p[i])
            densities.append(value[i])

    return p_values, densities


def get_scanlon_phase_diagram(min_rainfall, max_rainfall):
    rainfalls = list(range(min_rainfall, max_rainfall + 1))
    slope = 0.0008588
    intercept = -0.1702
    densities = [max(0, slope * rainfall + intercept) for rainfall in rainfalls]

    return rainfalls, densities


def get_cluster_distribution(folder, file_name):
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


if __name__ == '__main__':
    ####################################
    # Tricritical Directed Percolation #
    ####################################
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    q = 0
    p_values = [0.65, 0.7, 0.72, 0.74]
    percolation_threshold = 0.72
    percolation_density = 0.54

    # q = 0.25
    # p_values = [0.6, 0.62, 0.65, 0.67]
    # percolation_threshold = 0.65
    # percolation_density = 0.535

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]
    # percolation_threshold = 0.55
    # percolation_density = 0.53

    # q = 0.75
    # p_values = [0.405, 0.41, 0.42, 0.44]
    # percolation_threshold = 0.42
    # percolation_density = 0.52

    # q = 0.92
    # p_values = [0.282, 0.283, 0.285, 0.29]
    # densities = [0.878, 0.166, 0.4, 0.67]
    # percolation_threshold = 0.285
    # percolation_density = 0.4

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    num_cols = len(p_values)
    plt.subplots(2, num_cols, figsize=(20, 11))

    for i in tqdm(range(len(p_values))):
        col = i + 1
        p = p_values[i]
        folder_name= str(p).replace('.', 'p')

        row = 0
        birth_prob, densities = get_tricritical_phase_diagram(phase_diagram_path, q)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title(f"Phase diagram, p = {p}", fontsize=14)
        plt.xlabel("p", fontsize=12)

        if col == 1:
            plt.ylabel("density", fontsize=12)
        else:
            plt.yticks([])
        plt.plot(birth_prob, densities, label="steady state density")
        plt.plot(percolation_threshold, percolation_density, 'x', label="percolation threshold")

        # for q = 0.92
        # densities = [0.0878, 0.166, 0.4, 0.67]
        # plt.plot(p_values[i], densities[i], 'o', label="current point")

        # for everything else
        plt.plot(p, densities[birth_prob.index(p)], 'o', label="current point")
        plt.legend()

        row = 1
        file_name = f"{folder_name}_cluster_distribution.txt"
        cluster_sizes, inverse_cdf = get_cluster_distribution(folder_name, file_name)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title("Cluster size distribution (log-log)", fontsize=14)
        plt.xlabel("s", fontsize=12)

        if col == 1:
            plt.ylabel("P(S > s)", fontsize=12)
        plt.loglog(cluster_sizes, inverse_cdf, 'o')

    plt.savefig(subfolder + "_CSD.png", bbox_inches='tight')
    plt.show()

    ####################
    # Scanlon Kalahari #
    ####################
    # results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    # model = "scanlon_kalahari"
    # dataset = "100x100"
    # rainfall_values = [300, 500, 700, 900]

    # data_path = path.join(results_path, model, dataset)

    # num_cols = len(rainfall_values)
    # plt.subplots(2, num_cols, figsize=(20, 11))

    # for i in tqdm(range(num_cols)):
    #     col = i + 1
    #     rainfall = rainfall_values[i]
    #     folder_name = str(rainfall)

    #     row = 0
    #     rainfalls, densities = get_scanlon_phase_diagram(0, int(max(rainfall_values)) + 100)
    #     plt.subplot(2, num_cols, row * num_cols + col)
    #     plt.title(f"Phase diagram, rainfall = {rainfall}", fontsize=14)
    #     plt.xlabel("p", fontsize=12)

    #     if col == 1:
    #         plt.ylabel("density", fontsize=12)
    #     else:
    #         plt.yticks([])
    #     plt.plot(rainfalls, densities, label="steady state density")
    #     plt.plot(rainfall, densities[rainfalls.index(rainfall)], 'o', label="current point")
    #     plt.legend()

    #     row = 1
    #     file_name = f"{folder_name}_cluster_distribution.txt"
    #     cluster_sizes, inverse_cdf = get_cluster_distribution(folder_name, file_name)
    #     plt.subplot(2, num_cols, row * num_cols + col)
    #     plt.title("Cluster size distribution (log-log)", fontsize=14)
    #     plt.xlabel("s", fontsize=12)

    #     if col == 1:
    #         plt.ylabel("P(S > s)", fontsize=12)
    #     plt.loglog(cluster_sizes, inverse_cdf, 'o')

    # plt.savefig("scanlon_CSD.png", bbox_inches='tight')
    # plt.show()