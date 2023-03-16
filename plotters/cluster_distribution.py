from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros
from os import path
from tqdm import tqdm


def get_phase_diagram(q_value):
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
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100_2"

    q = 0
    p_values = [0.65, 0.7, 0.72, 0.74]

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]

    # q = 0.92
    # p_values = [0.28, 0.285, 0.29, 0.31]

    subfolder = "q" + str(q).replace('.', 'p')
    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)

    num_cols = len(p_values)
    plt.subplots(2, num_cols, figsize=(20, 10))

    for i in tqdm(range(len(p_values))):
        col = i + 1
        p = p_values[i]
        folder_name= str(p).replace('.', 'p')

        row = 0
        birth_prob, densities = get_phase_diagram(q)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title(f"Phase diagram for p = {p}")
        plt.xlabel("p")

        if col == 1:
            plt.ylabel("density")
        else:
            plt.yticks([])
        plt.plot(birth_prob, densities, label="steady state density")
        plt.plot(0.72, 0.54, 'x', label="percolation threshold")
        plt.plot(p, densities[birth_prob.index(p)], 'o', label="current point")
        plt.legend()

        row = 1
        file_name = f"{folder_name}_cluster_distribution.txt"
        cluster_sizes, inverse_cdf = get_cluster_distribution(folder_name, file_name)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title("Cluster size distribution (log-log)")
        plt.xlabel("s")

        if col == 1:
            plt.ylabel("P(S > s)")
        plt.loglog(cluster_sizes, inverse_cdf, 'o')

    plt.savefig(subfolder + "_CSD.png")
    plt.show()