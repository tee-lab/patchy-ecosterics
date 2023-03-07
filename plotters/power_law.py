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
    normalization = sum(num)

    for i in range(len(num)):
        inverse_cdf[i] = sum(num[i:]) / normalization

    remove_indices = []
    for i in range(len(cluster_sizes) - 1):
        if inverse_cdf[i] == inverse_cdf[i + 1]:
            remove_indices.append(i)

    cluster_sizes = delete(cluster_sizes, remove_indices)
    inverse_cdf = delete(inverse_cdf, remove_indices)

    return cluster_sizes, inverse_cdf


def get_cluster_dynamics(folder, file_name):
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

    return abs_changes[3:], abs_changes_histogram[3:]


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    subfolder = "q0"
    dataset = "optimized_fixed"

    phase_diagram_path = path.join(results_path, model)
    data_path = path.join(phase_diagram_path, subfolder, dataset)
    p_values = [0.65, 0.7, 0.72, 0.74]
    q = 0
    num_cols = len(p_values)

    plt.subplots(3, num_cols, figsize=(20, 15))

    for i in tqdm(range(len(p_values))):
        col = i + 1
        p = p_values[i]
        folder_name= str(p).replace('.', 'p')

        row = 0
        birth_prob, densities = get_phase_diagram(q)
        plt.subplot(3, len(p_values), row * num_cols + col)
        plt.title(f"p = {p}")
        plt.xlabel("p")
        plt.ylabel("density")
        plt.plot(birth_prob, densities)
        plt.plot(p, densities[birth_prob.index(p)], 'o')

        row = 1
        file_name = f"{folder_name}_cluster_distribution.txt"
        cluster_sizes, inverse_cdf = get_cluster_distribution(folder_name, file_name)
        plt.subplot(3, len(p_values), row * num_cols + col)
        plt.xlabel("s")
        plt.ylabel("P(S > s)")
        plt.loglog(cluster_sizes, inverse_cdf, 'o')

        row = 2
        file_name = f"{folder_name}_changes.txt"
        changes, changes_histogram = get_cluster_dynamics(folder_name, file_name)
        plt.subplot(3, len(p_values), row * num_cols + col)
        plt.xlabel("|dS|")
        plt.ylabel("P(|dS|)")
        plt.loglog(changes, changes_histogram)

    plt.savefig("power_law.png")
    plt.show()