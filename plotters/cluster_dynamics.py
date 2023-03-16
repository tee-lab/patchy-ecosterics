from matplotlib import pyplot as plt
from numpy import delete, loadtxt, transpose, zeros
from os import path
from tqdm import tqdm


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

    inverse_cdf = zeros(len(abs_changes_histogram))
    for i in range(len(abs_changes_histogram)):
        inverse_cdf[i] = sum(abs_changes_histogram[i:])
    inverse_cdf = inverse_cdf / sum(abs_changes_histogram)

    probability = zeros(len(abs_changes_histogram))
    probability[0] = sum(abs_changes_histogram)

    for i in range(1, len(abs_changes_histogram)):
        probability[i] = probability[i - 1] - abs_changes_histogram[i - 1]

    return abs_changes[3:], inverse_cdf[3:]


if __name__ == '__main__':
    results_path = path.join(path.dirname(path.dirname(__file__)), 'results')
    model = "tricritical"
    dataset = "100x100"

    # q = 0
    # p_values = [0.65, 0.7, 0.72, 0.74]

    # q = 0.5
    # p_values = [0.5, 0.53, 0.55, 0.57]

    q = 0.92
    p_values = [0.28, 0.285, 0.29, 0.31]

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
        file_name = f"{folder_name}_changes.txt"
        changes, inverse_cdf = get_cluster_dynamics(folder_name, file_name)
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title("Cluster dynamics (log-log)")
        plt.xlabel("|ds|")
        
        if col == 1:
            plt.ylabel("P(|dS| > |ds|)")

        plt.loglog(changes, inverse_cdf, 'o')

        row = 1
        plt.subplot(2, len(p_values), row * num_cols + col)
        plt.title("Cluster dynamics (semilogy)")
        plt.xlabel("|ds|")

        if col == 1:
            plt.ylabel("P(|dS| > |ds|)")
            
        plt.semilogy(changes, inverse_cdf, 'o')

    plt.savefig(subfolder + "_dynamics.png")
    plt.show()