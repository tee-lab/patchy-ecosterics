from matplotlib import pyplot as plt
from numpy import loadtxt, transpose
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


def get_mean_ds(name, limit):
    folder = path.join(data_path, name)
    cluster_ds_data = transpose(loadtxt(open(path.join(folder, name + '_cluster_ds.txt'), 'r')))
    cluster_analyze_limit = min(limit, len(cluster_ds_data[0]))
    cluster_ds_data = cluster_ds_data[1]

    return range(1, cluster_analyze_limit), cluster_ds_data[1:cluster_analyze_limit]


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    # q = 0
    # p_values = [0.71, 0.69, 0.67, 0.65]
    # cluster_limits = [1000, 300, 200, 100]
    # critical_threshold = 0.62
    # percolation_threshold = 0.72
    # percolation_density = 0.54

    q = 0.25
    p_values = [0.64, 0.62, 0.60, 0.58]
    cluster_limits = [1500, 300, 200, 100]
    critical_threshold = 0.57
    percolation_threshold = 0.65
    percolation_density = 0.535

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(results_path, model, subfolder, dataset)

    num_cols = len(p_values)
    plt.subplots(2, num_cols, figsize=(20, 11))

    for i in tqdm(range(num_cols)):
        col = i + 1
        p = p_values[i]
        limit = cluster_limits[i]
        folder_name= str(p).replace('.', 'p')

        row = 0
        birth_prob, densities = get_tricritical_phase_diagram(phase_diagram_path, q)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title(f"Phase diagram for p = {p}", fontsize=14)
        plt.xlabel("p", fontsize=12)

        if col == 1:
            plt.ylabel("density", fontsize=12)
        else:
            plt.yticks([])
        plt.plot(birth_prob, densities, label="steady state density")
        plt.plot(percolation_threshold, percolation_density, 'x', label="percolation threshold")
        plt.plot(critical_threshold, 0, 'x', label="critical threshold")
        plt.legend()

        plt.plot(p, densities[birth_prob.index(p)], 'o', label="current point")
        plt.legend()

        row = 1
        cluster_sizes, mean_ds_sq = get_mean_ds(folder_name, limit)
        plt.subplot(2, num_cols, row * num_cols + col)
        plt.title(f"Drift Term for p = {p}")
        plt.xlabel("Cluster Size", fontsize=12)

        if col == 1:
            plt.ylabel("Mean ds", fontsize=12)
        plt.plot(cluster_sizes, mean_ds_sq)
        plt.axhline(y=0, linestyle='--')

    plt.savefig(f"q{str(q).replace('.', 'p')}_ews3.png", bbox_inches='tight')
    plt.show()