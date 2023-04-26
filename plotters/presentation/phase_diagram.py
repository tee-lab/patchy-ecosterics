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
    results_path = path.join(path.dirname(path.dirname(__file__)), '..', 'results')
    model = "tricritical"
    dataset = "100x100"

    # q = 0
    # p_values = [0.65, 0.7, 0.72, 0.74]
    # percolation_threshold = 0.72
    # percolation_density = 0.54

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

    q = 0
    percolation_threshold = 0.72
    critical_threshold = 0.62

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    birth_prob, densities = get_tricritical_phase_diagram(phase_diagram_path, q)
    plt.title(f"Phase diagram of TDP across q = {q}", fontsize=14)
    plt.xlabel("p", fontsize=12)
    plt.ylabel("density", fontsize=12)
    plt.plot(birth_prob, densities, label="steady state density")
    plt.axvline(percolation_threshold, color='b', linestyle='--', label="percolation threshold")
    plt.axvline(critical_threshold, color='r', linestyle='--', label="critical threshold")
    plt.legend()
    plt.savefig(f"q{q}_phase_diagram.png")
    plt.show()