from numpy import delete, loadtxt, transpose, zeros
from matplotlib import pyplot as plt
from tqdm import tqdm
from os import path


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

    probability_distribution = abs_changes_histogram / sum(abs_changes_histogram)
    inverse_cdf = zeros(len(probability_distribution))
    for i in range(len(probability_distribution)):
        inverse_cdf[i] = sum(probability_distribution[i:])
    inverse_cdf = inverse_cdf / sum(inverse_cdf)

    return abs_changes[3:], inverse_cdf[3:]


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    q = 0
    p_values = [0.72, 0.69, 0.66, 0.63]
    critical_threshold = 0.62
    percolation_threshold = 0.72
    percolation_density = 0.54

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
        file_name = f"{folder_name}_changes.txt"
        changes, inverse_cdf = get_cluster_dynamics(folder_name, file_name)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title(f"Cluster dynamics (semilogy)", fontsize=14)
        plt.xlabel("|ds|", fontsize=12)

        if col == 1:
            plt.ylabel("P(|dS| > |ds|)", fontsize=12)
            
        plt.semilogy(changes, inverse_cdf, 'o')

    plt.savefig(f'q{str(q).replace(".", "p")}_ews2.png', bbox_inches='tight')
    plt.show()